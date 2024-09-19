from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from .database import get_db, Item

def read_all_items(request: Request, db: Session = Depends(get_db), ):
    db_items = db.query(Item)
    return db_items

def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
