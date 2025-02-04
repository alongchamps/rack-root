from fastapi import Depends, HTTPException, Request, status
from .database import getDb, DeviceType, Item
from .deviceType import getValidDeviceId
from sqlmodel import Session, select

## Reading items
def readAllItems(db: Session = Depends(getDb)):
    query = select(Item).join(DeviceType, isouter=True)
    results = db.exec(query)
    return results

def readItem(itemId: int, db: Session = Depends(getDb)):
    query = select(Item).where(Item.id == itemId).join(DeviceType, isouter=True)
    results = db.exec(query).first()

    if results is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return results

## Creating items
def createItem(item: Item, db: Session = Depends(getDb)):
    try:
        testDeviceId = getValidDeviceId(item.deviceTypeId, db)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    newItem = Item(**item.model_dump(exclude_unset=True))
    # newItem.deviceTypeId = getValidDeviceId(item.deviceTypeId, db)
    db.add(newItem)
    db.commit()
    db.refresh(newItem)

    return newItem

## Updating items
def updateItem(itemId: int, item: Item, db: Session = Depends(getDb)):
    # make sure we're getting a valid device ID, if provided
    if item.deviceTypeId != None:
        item.deviceTypeId = getValidDeviceId(item.deviceTypeId, db)
    
    statement = select(Item).where(Item.id == itemId)
    results = db.exec(statement)
    itemToUpdate = results.one()

    if itemToUpdate:
        for k, v in item.model_dump(exclude_unset=True).items():
            setattr(itemToUpdate, k, v)
    else:
        raise HTTPException(status_code=404, detail="An item with that ID was not found")

    db.add(itemToUpdate)
    db.commit()
    db.refresh(itemToUpdate)

    return 0

## Deleting items
def deleteItem(itemId: int, db: Session = Depends(getDb)):
    query = select(Item).where(Item.id == itemId)
    results = db.exec(query)
    try:
        itemToDelete = results.one()
        db.delete(itemToDelete)
        db.commit()
    except: 
        raise HTTPException(status_code=404, detail="An item with that ID was not found")

    return 0
