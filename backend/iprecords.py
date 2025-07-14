from devtools import pprint
from fastapi import Depends, HTTPException
from ipaddress import ip_network, ip_address
from sqlalchemy.orm import Session

from .database import getDb, IpRecord, Subnet

def getIpRecords(subnetId: int, db: Session = Depends(getDb)):
    results = db.query(IpRecord).where(IpRecord.subnetId == subnetId)
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

# def createIpRange(subnetId: int, db: Session = Depends(getDb)):
def createIpRange(subnet: Subnet, db: Session):

    # prep our records
    networkObjectForIpam = ip_network("{0}/{1}".format(subnet.network, str(subnet.subnetMaskBits)))
    for addr in networkObjectForIpam.hosts():
        try:
            db.add(IpRecord(status="Available", ipAddress=addr.compressed, subnetId=subnet.id))
        except:
            raise HTTPException(status_code=500, detail="iprecords.createIpRange - Issue creating the IP record in the database.")

    db.flush()

    return 0

def reserveIp(subnetId: int, ipAddress: str, reservationType: str, newDhcpRangeId: int, db: Session):

    updatedIpRecord = db.query(IpRecord).where(IpRecord.subnetId == subnetId).where(IpRecord.ipAddress == ipAddress).first()

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
        firstIp = db.query(IpRecord).where(IpRecord.id == ipAddressStartId).first()
    except:
        raise HTTPException(status_code=500, detail="iprecords.reserveIpRangeDhcp - Issue finding first IP when reserving for DHCP")

    try:
        lastIp = db.query(IpRecord).where(IpRecord.id == ipAddressEndId).first()
    except:
        raise HTTPException(status_code=500, detail="iprecords.reserveIpRangeDhcp - Issue finding last IP when reserving for DHCP")

    # prepare variables so we can loop over all IPs easily
    subnetObject = db.query(Subnet).where(Subnet.id == subnetId).first()
    firstIpObject = ip_address(firstIp.ipAddress)
    lastIpObject = ip_address(lastIp.ipAddress)

    # use ip_network to find all hosts
    networkObjectForDhcp = ip_network("{0}/{1}".format(subnetObject.network, str(subnetObject.subnetMaskBits)))
    for addr in networkObjectForDhcp.hosts():
        
        # if our IP is in the range of firstIp..lastIp, mark it as DHCP
        if addr >= firstIpObject and addr <= lastIpObject:
            reserveIp(subnetId=subnetId, ipAddress=addr.compressed, reservationType="DHCP", newDhcpRangeId=newDhcpRangeId, db=db)

    return 0

def clearIpAddress(subnetId: int, ipAddress: str, db: Session):
    try:
        updatedIpRecord = db.query(IpRecord).where(IpRecord.subnetId == subnetId).where(IpRecord.ipAddress == ipAddress).first()
    except:
        raise HTTPException(status_code=500, detail="iprecords.clearIpAddress - Issue finding record in the DB")

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
