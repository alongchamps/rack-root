from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import getDb, Item
from .deviceType import getValidDeviceId
from .validation_item import ItemCreate, ItemUpdate

## Reading items
def readAllItems(db: Session = Depends(getDb)):
    with db() as session:
        results = session.query(Item)
    return results

def readItem(itemId: int, db: Session = Depends(getDb)):
    with db() as session:
        results = session.query(Item).where(Item.id == itemId).first()

        if results is None:
            raise HTTPException(status_code=404, detail="Item not found")

    return results

## Creating items
def createItem(item: ItemCreate, db: Session = Depends(getDb)):
    with db() as session:
        try:
            testDeviceId = getValidDeviceId(item.deviceTypeId, db)
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        newItem = Item(**item.model_dump(exclude_unset=True))
        
        session.add(newItem)
        session.commit()
        session.refresh(newItem)

    return newItem

## Updating items
def updateItem(itemId: int, item: ItemUpdate, db: Session = Depends(getDb)):

    with db() as session:
        # make sure we're getting a valid device ID, if provided
        if item.deviceTypeId != None:
            item.deviceTypeId = getValidDeviceId(item.deviceTypeId, db)
        
        itemToUpdate = session.query(Item).where(Item.id == itemId).one()

        if itemToUpdate:
            for k, v in item.model_dump(exclude_unset=True).items():
                setattr(itemToUpdate, k, v)
        else:
            raise HTTPException(status_code=404, detail="An item with that ID was not found")

        session.add(itemToUpdate)
        session.commit()
        session.refresh(itemToUpdate)

    return 0

## Deleting items
def deleteItem(itemId: int, db: Session = Depends(getDb)):
    with db() as session:
        results = session.query(Item).where(Item.id == itemId)
        
        try:
            itemToDelete = results.one()
            session.delete(itemToDelete)
            session.commit()
        except: 
            raise HTTPException(status_code=404, detail="An item with that ID was not found")

    return 0
