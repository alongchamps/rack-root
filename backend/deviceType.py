from fastapi import Depends, HTTPException
from typing import Optional
from .database import getDb, DeviceType, Item
from sqlmodel import Session, select

# reading
def readAllDeviceTypes(db: Session = Depends(getDb)):
    query = select(DeviceType)
    results = db.exec(query)
    return results

def readDeviceType(devId: int, db: Session = Depends(getDb)):
    query = select(DeviceType).where(DeviceType.id == devId)
    results = db.exec(query).first()

    if results is None:
        raise HTTPException(status_code=404, detail="A device with that ID was not found")

    return results

def getValidDeviceId( devId: Optional[int] = None, db: Session = Depends(getDb) ) -> int:
    if devId is None:
        raise HTTPException(status_code=400, detail="Device type ID is required")

    query = select(DeviceType).where(DeviceType.id == devId)
    results = db.exec(query).first()
    
    if results is None:
        raise HTTPException(status_code=400, detail="Invalid device ID")
    
    return results.id

# creating
def createDeviceType(deviceType: DeviceType, db: Session = Depends(getDb)):
    newDeviceType = DeviceType(**deviceType.model_dump())
    db.add(newDeviceType)
    db.commit()
    db.refresh(newDeviceType)
    return newDeviceType

# Updating
def updateDeviceType(devId: int, devUpdate: DeviceType, db: Session = Depends(getDb)):
    # find our object from the database
    statement = select(DeviceType).where(DeviceType.id == devId)
    results = db.exec(statement)
    deviceToUpdate = results.one()

    if deviceToUpdate:
        for k, v in devUpdate.model_dump(exclude_unset=True).items():
            setattr(deviceToUpdate, k, v)
    else:
        raise HTTPException(status_code=404, detail="A device with that ID was not found")

    # want something like this to work
    # deviceToUpdate.update(**devUpdate.model_dump(exclude_unset=True))

    db.add(deviceToUpdate)
    db.commit()
    db.refresh(deviceToUpdate)

    return deviceToUpdate

## Deleting
def deleteDeviceType(devId: int, db: Session = Depends(getDb)):
    query = select(DeviceType).where(DeviceType.id == devId)
    results = db.exec(query)
    try:
        typeToDelete = results.one()
        db.delete(typeToDelete)
        db.commit()
    except: 
        raise HTTPException(status_code=404, detail="A device with that ID was not found")

    return 0
