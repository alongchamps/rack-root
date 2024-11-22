from pydantic import BaseModel
from typing import Optional

# Pydantic model for returning device types
class SubnetResponse(BaseModel):
    id: int
    name: str
    vlan: int
    classification: str
    network: str
    subnetMaskBits: int

# Pydantic model for creating device types
class SubnetCreate(BaseModel):
    name: str
    vlan: int
    classification: str
    network: str
    subnetMaskBits: int
