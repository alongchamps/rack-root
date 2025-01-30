from sqlmodel import SQLModel
from typing import List, Optional
from .database import IpRecord

class SubnetCreate(SQLModel):
    name: str
    vlan: int
    classification: str
    network: str
    subnetMaskBits: int
    # gateway: Optional[str] = None

class SubnetResponse(SQLModel):
    id: int
    name: str
    vlan: int
    classification: str
    network: str
    subnetMaskBits: int
    # gateway: Optional[str] = None
    ipam: Optional[list[IpRecord]] = None

class SubnetUpdateGateway(SQLModel):
    gateway: Optional[str] = None
