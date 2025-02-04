from .database import Item
from sqlmodel import SQLModel
from typing import Optional

class DeviceTypeResponse(SQLModel):
    id: int
    name: str
    items: list["Item"]

class DeviceTypeCreate(SQLModel):
    name: str

class DeviceTypeUpdate(SQLModel):
    name: Optional[str] = None
