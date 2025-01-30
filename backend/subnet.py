from fastapi import Depends, HTTPException
from ipaddress import ip_network,ip_address
from sqlmodel import Session, select

from .database import getDb, Subnet
from .iprecords import createIpRecord, reserveIp

# get all subnets from the database
def readAllSubnets(db: Session = Depends(getDb)):
    query = select(Subnet)
    results = db.exec(query)
    return results

# get data for one subnet
def readSingleSubnet(subnetId: int, db: Session = Depends(getDb)):
    query = select(Subnet).filter(Subnet.id == subnetId)
    results = db.exec(query).first()
    if results is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return results

# This function will make a new subnet as long as
#  (1) it's a valid network, 
#  (2) it doesn't overlap with an existing IP range,
#  (3) and hasn't been defined before
def createSubnet(subnet: Subnet, db: Session = Depends(getDb)):
    dbSubnet = Subnet(**subnet.model_dump())
    
    # 3 data validations before we save the network details to the database

    # (1) make sure we got an IP network, if any exception is thrown, we probably have bad data
    # for example, host bits are set (if network = 192.168.12.10 and subnet mask is /24, 
    # the network input really should be 192.168.12.0)
    try:
        validateNetwork = ip_network("{0}/{1}".format(dbSubnet.network, str(dbSubnet.subnetMaskBits)))
    except:
        raise HTTPException(status_code=400, detail="Invalid network provided")

    # (2) make sure the new range doesn't overlap with anything we already have
    query = select(Subnet)
    allNetworks = db.exec(query)
    for n in allNetworks:
        tmpNetwork = ip_network("{0}/{1}".format(n.network, str(n.subnetMaskBits)))
        if tmpNetwork.overlaps(validateNetwork):
            raise HTTPException(status_code=400, detail="Networks must be unique.")

    # (3) make sure we don't already have this network defined, this is not covered by (2)
    duplicateNetworkQuery = select(Subnet).where(Subnet.network == dbSubnet.network).where(Subnet.subnetMaskBits == dbSubnet.subnetMaskBits)
    duplicatedNetworkSearchResults = db.exec(duplicateNetworkQuery)

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
    newSubnetQuery = select(Subnet).where(Subnet.network == dbSubnet.network)
    newSubnet = db.exec(newSubnetQuery).first()

    # now make all of the IP records
    networkObjectForIpam = ip_network("{0}/{1}".format(newSubnet.network, str(newSubnet.subnetMaskBits)))
    for addr in networkObjectForIpam.hosts():
        try:
            createIpRecord(subnetId=newSubnet.id, ipAddress=addr.compressed, db=db)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=503, detail="subnet.createSubnet - issue making IPAM record...")

    # if a gateway is provided, save that in the database
    # if newSubnet.gateway is not None:
    #     reserveIp(subnetId=newSubnet.id, ipAddress=newSubnet.gateway, reservationType="gateway", db=db)

    return newSubnet

# delete a single subnet
def deleteSubnet(subnetId: int, db: Session = Depends(getDb)):
    query = select(Subnet).where(Subnet.id == subnetId)
    
    results = db.exec(query)
    if results is None:
        raise HTTPException(status_code=404, detail="A subnet with that ID was not found")
    
    try:
        subnetToDelete = results.one()
        db.delete(subnetToDelete)
        db.commit()
    except:
        raise HTTPException(status_code=500, detail="subnet.deleteSubnet - some DB error")
    
    return 0

# configure the gateway on a given network. This method can be used to clear a gateway, set a gateway,
# or update a gateway - all in one function
def setGateway(subnetId: int, incomingGateway: Subnet, db: Session = Depends(getDb)):

    # look for our database record
    query = select(Subnet).where(Subnet.id == subnetId)
    subnetToUpdate = db.exec(query).one()

    if subnetToUpdate is None:
        raise HTTPException(status_code=404, detail="Subnet not found")
    
    # if a gateway is provided, check that provided gateway is actually in this network
    if len(incomingGateway.gateway) > 0:
        
        validGateway = gatewayInSubnet(incomingGateway.gateway, subnetToUpdate.network, subnetToUpdate.subnetMaskBits)

        if validGateway == False:
            raise HTTPException(status_code=500, detail="Provided gateway is not in that subnet range.")

    # there is no else here because if the gateway is empty, the code/database will accept it and clear the record

    if subnetToUpdate:
        for k, v in incomingGateway.model_dump(exclude_unset=True).items():
            setattr(subnetToUpdate, k, v)

    # update the 
    try:
        db.add(subnetToUpdate)
        db.commit()
        db.refresh(subnetToUpdate)
    except:
        raise HTTPException(status_code=500, detail="Issue setting the gateway")

    return 0

# returns true or false if the gateway is in the provided network
def gatewayInSubnet(gateway: str, subnet: str, subnetMask: int):

    # error handling here makes sure we can cast the provided inputs
    # to the actual ip_address and ip_network types
    try:
        gateway_object = ip_address(gateway)
    except:
        raise HTTPException(status_code=500, detail="Issue converting provided input to an IP address")

    try:
        network_object = ip_network("{0}/{1}".format(subnet, subnetMask))
    except:
        raise HTTPException(status_code=500, detail="Issue converting provided input details to a network")
    
    return gateway_object in network_object.hosts()
