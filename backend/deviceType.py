from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from .database import get_db, DeviceType, DeviceTypeCreate

def read_all_device_types(request: Request, db: Session = Depends(get_db), ):
    db_items = db.query(DeviceType)
    return db_items

def create_device_type(item: DeviceTypeCreate, db: Session = Depends(get_db)):
    db_item = DeviceType(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

## Updating
# todo

## Deleting
# todo
