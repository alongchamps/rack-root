from pydantic import BaseModel
from typing import Optional

# Pydantic model for returning device types
class DeviceTypeResponse(BaseModel):
    id: int
    name: str

# Pydantic model for creating device types
class DeviceTypeCreate(BaseModel):
    name: str

# Pydantic model for updating a device
class DeviceTypeUpdate(BaseModel):
    name: Optional[str] = None
