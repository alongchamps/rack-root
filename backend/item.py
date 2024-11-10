from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from .database import get_db, Item, DeviceType

from .deviceType import get_valid_device_id
from .validation_item import ItemCreate, ItemUpdate

## Reading items
def read_all_items(request: Request, db: Session = Depends(get_db)):
    db_items = db.query(Item).join(DeviceType)
    return db_items

def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).join(DeviceType).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

## Creating items
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    item.deviceTypeId = get_valid_device_id(item.deviceTypeId, db)
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

## Updating items
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    # make sure we're getting a valid device ID, if provided
    if item.deviceTypeId != None:
        item.deviceTypeId = get_valid_device_id(item.deviceTypeId, db)

    # find our item ID in the database and update fields specified in the 'item' argument
    itemsAffected = db.query(Item).filter(Item.id == item_id).update(dict(**item.model_dump(exclude_unset=True)))
    db.commit()

    if itemsAffected == 0:
        raise HTTPException(status_code=404, detail="An item with that ID was not found")

    return itemsAffected

## Deleting items
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_delete = db.query(Item).filter(Item.id == item_id).delete(synchronize_session="auto")
    db.commit()

    if db_delete == 0:
        raise HTTPException(status_code=404, detail="An item with that ID was not found")

    return 0
