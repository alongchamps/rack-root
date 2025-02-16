from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from .database import DhcpRange, Subnet, IpRecord, getDb
from .iprecords import reserveIpRangeDhcp, clearIpAddress
from .validation_dhcpRange import DhcpCreate

def readSingleDhcpRange(dhcpId: int, db: Session = Depends(getDb)):
    query = select(DhcpRange).where(DhcpRange.id == dhcpId)
    try:
        results = db.exec(query).one()
    except:
        raise HTTPException(status_code=404, detail="A DHCP range with that ID was not found")

    return results

def newDhcpRange(newDhcpRange:DhcpCreate, subnetId: int, db: Session = Depends(getDb)):

    # make sure both IPs we got in are defined in the table
    try:
        firstIpQuery = select(IpRecord).where(IpRecord.subnetId == subnetId).where(IpRecord.ipAddress == newDhcpRange.startIp)
        # use .one() at the end of our results so that it will throw an informative error when 0 records are found
        firstIp = db.exec(firstIpQuery).one()
    except:
        raise HTTPException(status_code=400, detail="dhcpRange.newDhcpRange - First IP address not found in the database")
    
    try:
        lastIpQuery = select(IpRecord).where(IpRecord.subnetId == subnetId).where(IpRecord.ipAddress == newDhcpRange.endIp)
        # use .one() at the end of our results so that it will throw an informative error when 0 records are found
        lastIp = db.exec(lastIpQuery).one()
    except:
        raise HTTPException(status_code=400, detail="dhcpRange.newDhcpRange - Last IP address not found in the database")
    
    # make the record in the database
    try:
        newDhcpObject = DhcpRange(name=newDhcpRange.name, description=newDhcpRange.description, startIp=newDhcpRange.startIp, endIp=newDhcpRange.endIp)

        db.add(newDhcpObject)
        db.commit()
        db.refresh(newDhcpObject)
    except:
        raise HTTPException(status_code=400, detail="dhcpRange.newDhcpRange - Issue creating the DHCP range record in the database")

    # now that the record is created, reserve all of the IPs
    reserveIpRangeDhcp(subnetId=subnetId, ipAddressStartId=firstIp.id, ipAddressEndId=lastIp.id, newDhcpRangeId=newDhcpObject.id, db=db)

    return newDhcpObject

def deleteDhcpRange(subnetId:int, dhcpId:int, db: Session = Depends(getDb)):
    # find our subnet, else 404
    try:
        subnetQuery = select(Subnet).where(Subnet.id == subnetId)
        # use .one() at the end of our results so that it will throw an informative error when 0 records are found
        subnetResults = db.exec(subnetQuery).one()
    except:
        raise HTTPException(status_code=404, detail="dhcpRange.deleteDhcpRange - Provided subnet ID was not found in the database")

    # find our dhcpId, else 404
    try:
        dhcpRangeQuery = select(DhcpRange).where(DhcpRange.id == dhcpId)
        # use .one() at the end of our results so that it will throw an informative error when 0 records are found
        dhcpResults = db.exec(dhcpRangeQuery).one()
    except:
        raise HTTPException(status_code=404, detail="dhcpRange.deleteDhcpRange - Provided DHCP range ID was not found in this database")

    # find all IPs marked as being on this DHCP range (by dhcpRangeId) and delete them
    ipQuery = select(IpRecord).where(IpRecord.dhcpRangeId == dhcpId)
    ipResults = db.exec(ipQuery)

    for ipToClear in ipResults:
        clearIpAddress(subnetId=subnetId, ipAddress=ipToClear.ipAddress, db=db)

    # delete the record from the DHCP table
    try:
        db.delete(dhcpResults)
        db.commit()
    except: 
        raise HTTPException(status_code=404, detail="dhcpRange.deleteDhcpRange - Issue deleting that DHCP record from the database")

    return 0
