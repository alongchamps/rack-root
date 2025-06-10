from fastapi import Depends, HTTPException
from sqlalchemy import asc
from sqlalchemy.orm import Session
from typing import Optional

from .database import getDb, DeviceType, Item
from .validation_deviceType import DeviceTypeCreate, DeviceTypeUpdate

# Get all device types from the database
def readAllDeviceTypes(db: Session = Depends(getDb)):
    results = db.query(DeviceType).order_by(asc(DeviceType.name))

    return results

# query one device from the database
def readDeviceType(devId: int, db: Session = Depends(getDb)):
    results = db.query(DeviceType).filter(DeviceType.id == devId).first()

    if results is None:
        raise HTTPException(status_code=404, detail="A device with that ID was not found")

    return results

# Find the device ID if it is valid
def getValidDeviceId( devId: Optional[int] = None, db: Session = Depends(getDb) ) -> int:
    if devId is None:
        raise HTTPException(status_code=400, detail="Device type ID is required")

    results = db.query(DeviceType).filter(DeviceType.id == devId).first()
    
    if results is None:
        raise HTTPException(status_code=400, detail="Invalid device ID")
    
    return results.id

# Create a device type in the database
def createDeviceType(deviceType: DeviceTypeCreate, db: Session = Depends(getDb)):
    newDeviceType = DeviceType(**deviceType.model_dump())

    db.add(newDeviceType)
    db.commit()
    db.refresh(newDeviceType)

    return newDeviceType

# Update a device type's name (that's the only field supported by DeviceTypeUpdate)
def updateDeviceType(devId: int, devUpdate: DeviceTypeUpdate, db: Session = Depends(getDb)):
    
    deviceToUpdate = db.query(DeviceType).where(DeviceType.id == devId).first()

    # find our object from the database
    if deviceToUpdate:
        for k, v in devUpdate.model_dump(exclude_unset=True).items():
            setattr(deviceToUpdate, k, v)

    # if not found, error appropriately
    else:
        raise HTTPException(status_code=404, detail="A device with that ID was not found")

    db.add(deviceToUpdate)
    db.commit()
    db.refresh(deviceToUpdate)

    return deviceToUpdate

# Delete a given device ID from the database
def deleteDeviceType(devId: int, db: Session = Depends(getDb)):
    results = db.query(DeviceType).where(DeviceType.id == devId)

    try:
        typeToDelete = results.one()
        db.delete(typeToDelete)
        db.commit()
    except: 
        raise HTTPException(status_code=404, detail="A device with that ID was not found")

    return 0
