from datetime import date
from pydantic import BaseModel
from typing import Optional

from .validation_deviceType import DeviceTypeResponse

# Pydantic model for creating an item
class ItemCreate(BaseModel):
    name: str
    description: str
    deviceTypeId: int
    serialNumber: Optional[str] =  None
    purchaseDate: Optional[date] =  None
    warrantyExpiration: Optional[date] =  None
    notes: Optional[str] =  None

# Pydantic model for updating an item
class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    deviceTypeId: Optional[int] = None
    serialNumber: Optional[str] =  None
    purchaseDate: Optional[date] =  None
    warrantyExpiration: Optional[date] =  None
    notes: Optional[str] =  None

# Pydantic model for responding with an item
class ItemResponse(BaseModel):
    id: int
    name: str
    description: str
    deviceTypeId: int
    deviceType: DeviceTypeResponse
    serialNumber: str
    purchaseDate: date
    warrantyExpiration: date
    notes: str
