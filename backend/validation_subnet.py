from sqlmodel import SQLModel
from typing import List, Optional
from .database import IpRecord

class SubnetCreate(SQLModel):
    name: str
    vlan: int
    classification: str
    network: str
    subnetMaskBits: int

class SubnetResponse(SQLModel):
    id: int
    name: str
    vlan: int
    classification: str
    network: str
    subnetMaskBits: int
    ipam: Optional[list[IpRecord]] = None
