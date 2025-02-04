from datetime import datetime
from sqlmodel import SQLModel
from typing import Optional

from .validation_deviceType import DeviceTypeResponse

class ItemCreate(SQLModel):
    name: str
    description: Optional[str]
    deviceTypeId: int
    serialNumber: Optional[str] =  None
    purchaseDate: Optional[datetime] =  None
    warrantyExpiration: Optional[datetime] =  None
    notes: Optional[str] =  None
    DeviceType: DeviceTypeResponse = None

class ItemUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    deviceTypeId: Optional[int] = None
    serialNumber: Optional[str] =  None
    purchaseDate: Optional[datetime] =  None
    warrantyExpiration: Optional[datetime] =  None
    notes: Optional[str] =  None
    DeviceType: DeviceTypeResponse = None

class ItemResponse(SQLModel):
    id: int
    name: str
    description: Optional[str]
    deviceTypeId: int
    deviceType: DeviceTypeResponse
    serialNumber: Optional[str] =  None
    purchaseDate: Optional[datetime] =  None
    warrantyExpiration: Optional[datetime] =  None
    notes: Optional[str] = None
    DeviceType: DeviceTypeResponse = None
