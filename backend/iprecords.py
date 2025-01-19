from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db, IpRecord
from ipaddress import ip_network, ip_address

def get_ip_records(network_id: int, db: Session = Depends(get_db)):
    db_items = db.query(IpRecord).filter(IpRecord.subnet_id == network_id)
    return db_items

# todo: make this more efficient by batching up DB requests
# perhaps there's a way to make these all at once?
def create_ip_record(network_id: int, ip_address: str, db: Session = Depends(get_db)):
    # set inputs 
    ip_record = IpRecord()
    ip_record.subnet_id = network_id
    ip_record.status = "Available"
    ip_record.ipaddress = ip_address

    # save the data to the database here
    try:
        db.add(ip_record)
        db.commit()
        db.refresh(ip_record)
    except:
        raise HTTPException(status_code=500, detail="Issue creating the network in the database.")

    return 0

def reserve_ip(network_id: int, ip_address: str, db: Session = Depends(get_db)):
    return 0

def reserve_ip_dhcp(network_id: int, ip_address_start: str, ip_address_end: str, db: Session = Depends(get_db)):
    return 0

def clear_ip_address(network_id: int, ip_address: str, db: Session = Depends(get_db)):
    return 0
