from fastapi import Depends, HTTPException
from ipaddress import ip_network, ip_address
from sqlalchemy.orm import Session

from .database import getDb, IpRecord, Subnet

def getIpRecords(subnetId: int, db: Session = Depends(getDb)):
    with db() as session:
        results = session.query(IpRecord).where(IpRecord.subnetId == subnetId).join(Subnet, IpRecord.subnetId == Subnet.id)
    return results

def createIpRecord(subnetId: int, ipAddress: str, db: Session):
    with db() as session:
        newIpRecord = IpRecord(status="Available", ipAddress=ipAddress, subnetId=subnetId)
        
        try:
            session.add(newIpRecord)
            session.commit()
            session.refresh(newIpRecord)
        except:
            raise HTTPException(status_code=500, detail="iprecords.createIpRecord - Issue creating the IP record in the database.")

    return 0

def createIpRange(subnetId: int, db: Session):
    with db() as session:
        # get subnet from the database
        subnetObject = session.query(Subnet).where(Subnet.id == subnetId).first()

        # prep our records
        networkObjectForIpam = ip_network("{0}/{1}".format(subnetObject.network, str(subnetObject.subnetMaskBits)))
        for addr in networkObjectForIpam.hosts():
            try:
                session.add(IpRecord(status="Available", ipAddress=addr.compressed, subnetId=subnetId))
            except:
                raise HTTPException(status_code=500, detail="iprecords.createIpRange - Issue creating the IP record in the database.")

        session.commit()

    return 0

def reserveIp(subnetId: int, ipAddress: str, reservationType: str, newDhcpRangeId: int, db: Session):

    # with db() as session:
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

    # with db() as session:
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

    # TODO: refactor this so we summarize an IP range for a given subnet
    # then I can loop over all IPs in those networks^* and mark them as reserved.
    # I *think* this will be a little more performant.
    #
    # ^* when I call the ip_address -> summarize IP range, it returns an array of network objects
    # for example 10.0.1.10/28, 10.0.1.14/28, 10.0.1.18/32

    # use ip_network to find all hosts
    networkObjectForDhcp = ip_network("{0}/{1}".format(subnetObject.network, str(subnetObject.subnetMaskBits)))
    for addr in networkObjectForDhcp.hosts():
        
        # if our IP is in the range of firstIp..lastIp, mark it as DHCP
        if addr >= firstIpObject and addr <= lastIpObject:
            # reserveIp(subnetId=subnetId, ipAddress=addr.compressed, reservationType="DHCP", newDhcpRangeId=newDhcpRangeId, db=db)
            reserveIp(subnetId=subnetId, ipAddress=addr.compressed, reservationType="DHCP", newDhcpRangeId=newDhcpRangeId, db=db)

    # now that our IPs are all marked as assigned, make the DHCP reservation 

    return 0

def clearIpAddress(subnetId: int, ipAddress: str, db: Session = Depends(getDb)):
    with db() as session:
        try:
            updatedIpRecord = session.query(IpRecord).where(IpRecord.subnetId == subnetId).where(IpRecord.ipAddress == ipAddress).first()
        except:
            raise HTTPException(status_code=501, detail="iprecords.clearIpAddress - Issue finding record in the DB")

        updatedIpRecord.status = "Available"

        if updatedIpRecord.dhcpRangeId is not None:
            updatedIpRecord.dhcpRangeId = None

        try:
            session.add(updatedIpRecord)
            session.commit()
            session.refresh(updatedIpRecord)
        except:
            raise HTTPException(status_code=502, detail="iprecords.clearIpAddress - Issue assigning a status to an IP record in the database.")
        
    return 0
