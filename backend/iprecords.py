from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from .database import getDb, IpRecord, Subnet
from ipaddress import ip_network, ip_address, summarize_address_range

# def getIpRecords(networkId: int, db: Session = Depends(getDb)):
def getIpRecords(subnetId: int, db: Session = Depends(getDb)):
    query = select(IpRecord).where(IpRecord.subnetId == subnetId)
    results = db.exec(query)
    return results

def createIpRecord(subnetId: int, ipAddress: str, db: Session):
    newIpRecord = IpRecord(status="Available", ipAddress=ipAddress, subnetId=subnetId)
    
    try:
        db.add(newIpRecord)
        db.commit()
        db.refresh(newIpRecord)
    except:
        raise HTTPException(status_code=500, detail="iprecords.createIpRecord - Issue creating the IP record in the database.")

    return 0

def createIpRange(subnetId: int, db: Session):
    # get subnet from the database
    subnetQuery = select(Subnet).where(Subnet.id == subnetId)
    subnetObject = db.exec(subnetQuery).first()

    # prep our records

    networkObjectForIpam = ip_network("{0}/{1}".format(subnetObject.network, str(subnetObject.subnetMaskBits)))
    for addr in networkObjectForIpam.hosts():
        try:
            db.add(IpRecord(status="Available", ipAddress=addr.compressed, subnetId=subnetId))
        except:
            raise HTTPException(status_code=500, detail="iprecords.createIpRange - Issue creating the IP record in the database.")

    db.commit()
    # db.refresh()

    return 0

def reserveIp(subnetId: int, ipAddress: str, reservationType: str, newDhcpRangeId: int, db: Session):
    query = select(IpRecord).where(IpRecord.subnetId == subnetId).where(IpRecord.ipAddress == ipAddress)
    updatedIpRecord = db.exec(query).first()

    # check that the IP isn't already reserved
    if updatedIpRecord.status != "Available":
        raise HTTPException(status_code=400, detail="iprecords.reserveIp - The IP you're attempting to reserve is already assigned.")

    updatedIpRecord.status = reservationType

    if newDhcpRangeId is not None:
        updatedIpRecord.dhcpRangeId = newDhcpRangeId

    try:
        db.add(updatedIpRecord)
        db.commit()
        db.refresh(updatedIpRecord)
    except:
        raise HTTPException(status_code=500, detail="iprecords.reserveIp - Issue assigning a status to an IP record in the database.")

    return 0

def reserveIpRangeDhcp(subnetId: int, ipAddressStartId: int, ipAddressEndId: int, newDhcpRangeId: int, db: Session):
    try:
        firstIpQuery = select(IpRecord).where(IpRecord.id == ipAddressStartId)
        firstIp = db.exec(firstIpQuery).first()
    except:
        raise HTTPException(status_code=500, detail="iprecords.reserveIpRangeDhcp - Issue finding first IP when reserving for DHCP")

    try:
        lastIpQuery = select(IpRecord).where(IpRecord.id == ipAddressEndId)
        lastIp = db.exec(lastIpQuery).first()
    except:
        raise HTTPException(status_code=500, detail="iprecords.reserveIpRangeDhcp - Issue finding last IP when reserving for DHCP")

    # prepare variables so we can loop over all IPs easily
    subnetQuery = select(Subnet).where(Subnet.id == subnetId)
    subnetObject = db.exec(subnetQuery).first()
    firstIpObject = ip_address(firstIp.ipAddress)
    lastIpObject = ip_address(lastIp.ipAddress)

    #TODO: refactor this so we summarize an IP range for a given subnet
    # then I can loop over all IPs in those networks^* and mark them as reserved.
    # I *think* this will be a little more performant.
    #
    # ^* when I call the ip_address -> summarize IP range, it returns an array of network objects
    # for example 10.0.1.10/28, 10.0.1.14/28, 10.0.1.18/32

    networkObjectForDhcp = ip_network("{0}/{1}".format(subnetObject.network, str(subnetObject.subnetMaskBits)))
    for addr in networkObjectForDhcp.hosts():
        
        # if our IP is in the range of firstIp..lastIp, mark it as DHCP
        if addr >= firstIpObject and addr <= lastIpObject:
            reserveIp(subnetId=subnetId, ipAddress=addr.compressed, reservationType="DHCP", newDhcpRangeId=newDhcpRangeId, db=db)

    # now that our IPs are all marked as assigned, make the DHCP reservation 

    return 0

def clearIpAddress(subnetId: int, ipAddress: str, db: Session):
    query = select(IpRecord).where(IpRecord.subnetId == subnetId).where(IpRecord.ipAddress == ipAddress)
    updatedIpRecord = db.exec(query).first()

    updatedIpRecord.status = "Available"

    if updatedIpRecord.dhcpRangeId is not None:
        updatedIpRecord.dhcpRangeId = None

    try:
        db.add(updatedIpRecord)
        db.commit()
        db.refresh(updatedIpRecord)
    except:
        raise HTTPException(status_code=500, detail="iprecords.clearIpAddress - Issue assigning a status to an IP record in the database.")
    
    return 0
