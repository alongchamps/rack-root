from fastapi import Depends, HTTPException
from ipaddress import ip_network,ip_address
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from .database import getDb, Subnet, IpRecord
from .iprecords import createIpRecord, clearIpAddress, createIpRange
from .validation_iprecord import IpRecordGateway
from .validation_subnet import SubnetCreate

# get all subnets from the database
def readAllSubnets(db: sessionmaker = Depends(getDb)):
    results = db.query(Subnet)
    return results

# get data for one subnet
def readSingleSubnet(subnetId: int, db: sessionmaker = Depends(getDb)):
    results = db.query(Subnet).where(Subnet.id == subnetId).first()

    if results is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return results

# This function will make a new subnet as long as
#  (1) it's a valid network, 
#  (2) it doesn't overlap with an existing IP range,
#  (3) and hasn't been defined before
def createSubnet(subnet: SubnetCreate, db: sessionmaker = Depends(getDb)):
    dbSubnet = Subnet(**subnet.model_dump(exclude_unset=True))

    # (1) make sure we got an IP network, if any exception is thrown, we probably have bad data
    # for example, host bits are set (if network = 192.168.12.10 and subnet mask is /24, 
    # the network input really should be 192.168.12.0)
    try:
        validateNetwork = ip_network("{0}/{1}".format(dbSubnet.network, str(dbSubnet.subnetMaskBits)))
    except:
        raise HTTPException(status_code=400, detail="Invalid network provided")

    # (2) make sure the new range doesn't overlap with anything we already have
    # query = select(Subnet)
    # allNetworks = db.exec(query)
    
    allNetworks = db.query(Subnet)

    for n in allNetworks:
        tmpNetwork = ip_network("{0}/{1}".format(n.network, str(n.subnetMaskBits)))
        if tmpNetwork.overlaps(validateNetwork):
            raise HTTPException(status_code=400, detail="Networks must be unique.")

    # (3) make sure we don't already have this network defined, this is not covered by (2)
    # duplicateNetworkQuery = select(Subnet).where(Subnet.network == dbSubnet.network).where(Subnet.subnetMaskBits == dbSubnet.subnetMaskBits)
    # duplicatedNetworkSearchResults = db.exec(duplicateNetworkQuery)

    duplicatedNetworkSearchResults = db.query(Subnet).where(Subnet.network == dbSubnet.network).where(Subnet.subnetMaskBits == dbSubnet.subnetMaskBits)

    # if we have any results here, we have a duplicate
    for duplicate in duplicatedNetworkSearchResults:
        raise HTTPException(status_code=400, detail="This network seems to already exist.")

    # save the data to the database here
    try:
        db.add(dbSubnet)
        db.commit()
        db.refresh(dbSubnet)
    except:
        raise HTTPException(status_code=400, detail="Issue creating the network in the database.")
    
    # get the database result, especially so we can read the ID
    # newSubnetQuery = select(Subnet).where(Subnet.network == dbSubnet.network)
    # newSubnet = db.exec(newSubnetQuery).first()

    newSubnet = db.query(Subnet).where(Subnet.network == dbSubnet.network).first()

    createIpRange(subnetId=newSubnet.id, db=db)

    # db.refresh(dbSubnet)

    # now make all of the IP records - old and slow
    # networkObjectForIpam = ip_network("{0}/{1}".format(newSubnet.network, str(newSubnet.subnetMaskBits)))
    # for addr in networkObjectForIpam.hosts():
    #     try:
    #         createIpRecord(subnetId=newSubnet.id, ipAddress=addr.compressed, db=db)
    #     except Exception as e:
    #         print(e)
    #         raise HTTPException(status_code=400, detail="subnet.createSubnet - issue making IPAM record...")

    return dbSubnet

# delete a single subnet
def deleteSubnet(subnetId: int, db: sessionmaker = Depends(getDb)):
    # query = select(Subnet).where(Subnet.id == subnetId)
    # results = db.exec(query)

    results = db.query(Subnet).where(Subnet.id == subnetId)

    if results is None:
        raise HTTPException(status_code=404, detail="A subnet with that ID was not found")
    
    try:
        subnetToDelete = results.one()
        db.delete(subnetToDelete)
        db.commit()
    except:
        raise HTTPException(status_code=500, detail="subnet.deleteSubnet - some DB error")
    
    return 0

# find the gateway associated with this subnet, from the IpRecord table, if it exists
def readGateway(subnetId: int, db: sessionmaker = Depends(getDb)):
    # query = select(IpRecord).where(IpRecord.subnetId == subnetId).where(IpRecord.status == "Gateway")
    try:
        # results = db.exec(query).one()
        results = db.query(IpRecord).where(IpRecord.subnetId == subnetId).where(IpRecord.status == "Gateway").one()
    except:
        return None

    return results

# This function set the gateway for the provided subnetId, by updating the IpAddress table.
# The first query will find the relevant IP record, which has an added bonus of also making
# sure the provided gateway is in the network. If no result comes back, the IP / subnet 
# relationship is wrong. This function call also clears an existing gateway if it is found.
def setGateway(subnetId: int, incomingGateway: IpRecordGateway, db: sessionmaker = Depends(getDb)):
    # find our IpRecord
    # ipRecordQuery = select(IpRecord).where(IpRecord.subnetId == subnetId).where(IpRecord.ipAddress == incomingGateway.gateway)
    try:
        # ipRecordToupdate = db.exec(ipRecordQuery).one()
        ipRecordToUpdate = db.query(IpRecord).where(IpRecord.subnetId == subnetId).where(IpRecord.ipAddress == incomingGateway.gateway).one()
    except:
        raise HTTPException(status_code=500, detail="No matching IP records found. Is that IP on that network?")

    # clear an existing record, if found
    deleteGateway(subnetId, db)

    ipRecordToUpdate.status = "Gateway"

    try:
        db.add(ipRecordToUpdate)
        db.commit()
        db.refresh(ipRecordToUpdate)
    except:
        raise HTTPException(status_code=500, detail="Issue setting the gateway")

    return incomingGateway

# find IP records on subnetId with the status 'Gateway', and change that to 'Available'
def deleteGateway(subnetId: int, db: sessionmaker = Depends(getDb)):
    # query = select(IpRecord).where(IpRecord.subnetId == subnetId).where(IpRecord.status == "Gateway")
    try:
        # results = db.exec(query).one()
        results = db.query(IpRecord).where(IpRecord.subnetId == subnetId).where(IpRecord.status == "Gateway").one()
    except:
        return None

    if results is not None:    
        clearIpAddress(subnetId, results.ipAddress, db)

    return None

# returns true or false if the gateway is in the provided network
def gatewayInSubnet(gateway: str, subnet: str, subnetMask: int):

    # error handling here makes sure we can cast the provided inputs
    # to the actual ip_address and ip_network types
    try:
        gatewayObject = ip_address(gateway)
    except:
        raise HTTPException(status_code=500, detail="Issue converting provided input to an IP address")

    try:
        networkObject = ip_network("{0}/{1}".format(subnet, subnetMask))
    except:
        raise HTTPException(status_code=500, detail="Issue converting provided input details to a network")
    
    return gatewayObject in networkObject.hosts()
