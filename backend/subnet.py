from devtools import pprint
from fastapi import Depends, HTTPException
from ipaddress import ip_network,ip_address
from sqlalchemy import inspect
from sqlalchemy.orm import Session, selectinload, joinedload, lazyload

from .database import getDb, Subnet, IpRecord
from .iprecords import clearIpAddress, createIpRange
from .validation_iprecord import IpRecordGateway
from .validation_subnet import SubnetCreate

import traceback

# get all subnets from the database
def readAllSubnets(db: Session = Depends(getDb)):
    results = db.query(Subnet)
    return results

# get data for one subnet
def readSingleSubnet(subnetId: int, db: Session = Depends(getDb)):
    results = db.query(Subnet).options(joinedload(Subnet.ipRecord)).where(Subnet.id == subnetId).first()

    if results is None:
        raise HTTPException(status_code=404, detail="subnet.readSingleSubnet - Item not found")

    return results

# This function will make a new subnet as long as
#  (1) it's a valid network, 
#  (2) it doesn't overlap with an existing IP range,
#  (3) and hasn't been defined before
def createSubnet(subnet: SubnetCreate, db: Session = Depends(getDb)):
    dbSubnet = Subnet(**subnet.model_dump(exclude_unset=True))
    network = dbSubnet.network

    # pprint(dbSubnet)
    
    # (1) make sure we got an IP network, if any exception is thrown, we probably have bad data
    # for example, host bits are set (if network = 192.168.12.10 and subnet mask is /24, 
    # the network input really should be 192.168.12.0)
    try:
        validateNetwork = ip_network("{0}/{1}".format(dbSubnet.network, str(dbSubnet.subnetMaskBits)))
    except:
        raise HTTPException(status_code=400, detail="subnet.createSubnet - Invalid network provided")

    # (2) make sure the new range doesn't overlap with anything we already have
    allNetworks = db.query(Subnet)

    for n in allNetworks:
        tmpNetwork = ip_network("{0}/{1}".format(n.network, str(n.subnetMaskBits)))
        if tmpNetwork.overlaps(validateNetwork):
            raise HTTPException(status_code=400, detail="subnet.createSubnet - Networks must be unique.")

    # (3) make sure we don't already have this network defined, this is not covered by (2)
    duplicatedNetworkSearchResults = db.query(Subnet).where(Subnet.network == dbSubnet.network).where(Subnet.subnetMaskBits == dbSubnet.subnetMaskBits)

    # if we have any results here, we have a duplicate
    for duplicate in duplicatedNetworkSearchResults:
        raise HTTPException(status_code=400, detail="subnet.createSubnet - This network seems to already exist.")

    # save the data to the database here
    db.add(dbSubnet)
    db.flush()

    try:
        createIpRange(subnet=dbSubnet, db=db)
    except:
        raise HTTPException(status_code=400, detail="subnet.createSubnet - Issue allocating all IPs")

    db.commit()
    db.refresh(dbSubnet)

    return dbSubnet

# delete a single subnet
def deleteSubnet(subnetId: int, db: Session = Depends(getDb)):
    
    results = db.query(Subnet).where(Subnet.id == subnetId)

    if results is None:
        raise HTTPException(status_code=404, detail="subnet.deleteSubnet - A subnet with that ID was not found")
    
    try:
        subnetToDelete = results.one()
        db.delete(subnetToDelete)
        db.commit()
    except:
        raise HTTPException(status_code=500, detail="subnet.deleteSubnet - some DB error")
    
    return None

# find the gateway associated with this subnet, from the IpRecord table, if it exists
def readGateway(subnetId: int, db: Session = Depends(getDb)):
    try:
        results = db.query(IpRecord).where(IpRecord.subnetId == subnetId).where(IpRecord.status == "Gateway").one()
    except:
        raise HTTPException(status_code=404, detail="subnet.readGateway - No gateway on that network")

    return results

# This function set the gateway for the provided subnetId, by updating the IpAddress table.
# The first query will find the relevant IP record, which has an added bonus of also making
# sure the provided gateway is in the network. If no result comes back, the IP / subnet 
# relationship is wrong. This function call also clears an existing gateway if it is found.
def setGateway(subnetId: int, incomingGateway: IpRecordGateway, db: Session = Depends(getDb)):
    
    try:
        # find our IpRecord
        ipRecord = db.query(IpRecord).where(IpRecord.subnetId == subnetId).where(IpRecord.ipAddress == incomingGateway.ipAddress).one()
    except:
        raise HTTPException(status_code=500, detail="subnet.setGateway - No matching IP records found. Is that IP on that network?")

    # clear an existing record, if found
    try:
        results = db.query(IpRecord).where(IpRecord.subnetId == subnetId).where(IpRecord.status == "Gateway").one()
    except:
        results = None

    if results is not None:    
        clearIpAddress(subnetId, results.ipAddress, db)

    ipRecord.status = "Gateway"

    try:
        db.add(ipRecord)
        db.commit()
        db.refresh(ipRecord)
    except:
        raise HTTPException(status_code=500, detail="subnet.setGateway - Issue setting the gateway")

    return ipRecord

# find IP records on subnetId with the status 'Gateway', and change that to 'Available'
def deleteGateway(subnetId: int, db: Session = Depends(getDb)):
    try:
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
        raise HTTPException(status_code=500, detail="subnet.gatewayInSubnet - Issue converting provided input to an IP address")

    try:
        networkObject = ip_network("{0}/{1}".format(subnet, subnetMask))
    except:
        raise HTTPException(status_code=500, detail="subnet.gatewayInSubnet - Issue converting provided input details to a network")
    
    # now see if the gateway is in the subnet
    return gatewayObject in networkObject.hosts()
