from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from .database import getDb, IpRecord
from ipaddress import ip_network, ip_address

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

def reserveIp(subnetId: int, ipAddress: str, reservationType: str, db: Session):
    query = select(IpRecord).where(IpRecord.subnetId == subnetId).where(IpRecord.ipAddress == ipAddress)
    updatedIpRecord = db.exec(query).first()

    updatedIpRecord.status = reservationType

    try:
        db.add(updatedIpRecord)
        db.commit()
        db.refresh(updatedIpRecord)
    except:
        raise HTTPException(status_code=500, detail="iprecords.reserveIp - Issue assigning a status to an IP record in the database.")

    return 0

def reserveIpDhcp(subnetId: int, ipAddressStart: str, ipAddressEnd: str, db: Session):
    # todo
    return 0

def clearIpAddress(subnetId: int, ipAddress: str, db: Session):
    query = select(IpRecord).where(IpRecord.subnetId == subnetId).where(IpRecord.ipAddress == ipAddress)
    updatedIpRecord = db.exec(query).first()

    updatedIpRecord.status = "Available"

    try:
        db.add(updatedIpRecord)
        db.commit()
        db.refresh(updatedIpRecord)
    except:
        raise HTTPException(status_code=500, detail="iprecords.clearIpAddress - Issue assigning a status to an IP record in the database.")
    
    return 0
