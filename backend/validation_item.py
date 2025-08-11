from datetime import datetime
from pydantic import BaseModel
from typing import Optional

# A copy of ItemResponse but without the reference to device type
class ItemResponseOnly(BaseModel):
    id: int
    name: str
    description: Optional[str]
    serialNumber: Optional[str] =  None
    purchaseDate: Optional[datetime] =  None
    warrantyExpiration: Optional[datetime] =  None
    notes: Optional[str] = None

# begin classes that have relations to other models

from .validation_deviceType import DeviceTypeResponseOnly

class ItemCreate(BaseModel):
    name: str
    description: Optional[str]
    deviceTypeId: int
    serialNumber: Optional[str] =  None
    purchaseDate: Optional[datetime] =  None
    warrantyExpiration: Optional[datetime] =  None
    notes: Optional[str] =  None
    DeviceType: DeviceTypeResponseOnly = None

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    deviceTypeId: Optional[int] = None
    serialNumber: Optional[str] =  None
    purchaseDate: Optional[datetime] =  None
    warrantyExpiration: Optional[datetime] =  None
    notes: Optional[str] =  None
    DeviceType: DeviceTypeResponseOnly = None

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    serialNumber: Optional[str] =  None
    purchaseDate: Optional[datetime] =  None
    warrantyExpiration: Optional[datetime] =  None
    notes: Optional[str] = None
    deviceTypeId: int
    deviceType: DeviceTypeResponseOnly = None
