from pydantic import BaseModel
from typing import Optional

# A copy of DeviceTypeResponse without the items attribute
class DeviceTypeResponseOnly(BaseModel):
    id: int
    name: str

class DeviceTypeCreate(BaseModel):
    name: str

class DeviceTypeUpdate(BaseModel):
    name: Optional[str] = None

# begin classes that have relations to other models
from .validation_item import ItemResponseOnly

class DeviceTypeResponse(BaseModel):
    id: int
    name: str
    item: list[ItemResponseOnly]
