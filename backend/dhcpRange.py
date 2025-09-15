from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from .database import DhcpRange, Subnet, IpRecord, getDb
from .iprecords import reserveIpRangeDhcp, clearIpAddress
from .validation_dhcpRange import DhcpCreate

def readDhcpRangesBySubnet(subnetId: int, db: Session = Depends(getDb)):
    results = db.query(DhcpRange).where(DhcpRange.subnetId == subnetId)

    return results

def readSingleDhcpRange(dhcpId: int, db: Session = Depends(getDb)):
    try:
        results = db.query(DhcpRange).where(DhcpRange.id == dhcpId).one()
    except:
        raise HTTPException(status_code=404, detail="A DHCP range with that ID was not found")

    return results

def newDhcpRange(newDhcpRange:DhcpCreate, subnetId: int, db: Session = Depends(getDb)):

    # make sure both IPs we got in are defined in the table
    # this is done by looking for a record where we should get one result and if .one() throws an error, we have an issue
    try:
        firstIp = db.query(IpRecord).where(IpRecord.subnetId == subnetId).where(IpRecord.ipAddress == newDhcpRange.startIp).one()
    except:
        raise HTTPException(status_code=400, detail="dhcpRange.newDhcpRange - First IP address not found in the database")
    
    try:
        lastIp = db.query(IpRecord).where(IpRecord.subnetId == subnetId).where(IpRecord.ipAddress == newDhcpRange.endIp).one()
    except:
        raise HTTPException(status_code=400, detail="dhcpRange.newDhcpRange - Last IP address not found in the database")
    
    # make the record in the database
    try:
        newDhcpObject = DhcpRange(**newDhcpRange.model_dump(exclude_unset=True))
        newDhcpObject.subnetId = subnetId

        db.add(newDhcpObject)
        db.commit()
        db.refresh(newDhcpObject)
    except:
        db.delete(newDhcpObject)
        db.commit()
        raise HTTPException(status_code=400, detail="dhcpRange.newDhcpRange - Issue creating the DHCP range record in the database")

    firstIp2 = db.merge(firstIp)
    lastIp2 = db.merge(lastIp)

    # now that the record is created, reserve all of the IPs
    reserveIpRangeDhcp(subnetId=subnetId, ipAddressStartId=firstIp2.id, ipAddressEndId=lastIp2.id, newDhcpRangeId=newDhcpObject.id, db=db)

    # call session.merge to refresh our references to newDhcpObject and return it all in one
    return db.merge(newDhcpObject)

def deleteDhcpRange(subnetId:int, dhcpId:int, db: Session = Depends(getDb)):

    # find our subnet, else 404
    try:
        # use .one() at the end of our results so that it will throw an informative error when 0 records are found
        subnetResults = db.query(Subnet).where(Subnet.id == subnetId).one()
    except:
        raise HTTPException(status_code=404, detail="dhcpRange.deleteDhcpRange - Provided subnet ID was not found in the database")

    # find our dhcpId, else 404
    try:
        dhcpResults = db.query(DhcpRange).where(DhcpRange.id == dhcpId).one()
    except:
        raise HTTPException(status_code=404, detail="dhcpRange.deleteDhcpRange - Provided DHCP range ID was not found in this database")

    # find all IPs marked as being on this DHCP range (by dhcpRangeId) and delete them
    ipResults = db.query(IpRecord).where(IpRecord.dhcpRangeId == dhcpId)

    for ipToClear in ipResults:
        clearIpAddress(subnetId=subnetId, ipAddress=ipToClear.ipAddress, db=db)

    # delete the record from the DHCP table
    try:
        db.delete(dhcpResults)
        db.commit()
    except: 
        raise HTTPException(status_code=503, detail="dhcpRange.deleteDhcpRange - Issue deleting that DHCP record from the database")

    return 0
