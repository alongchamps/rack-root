from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Mapped, relationship
from .database import IpRecord

# Pydantic model for returning subnets
class SubnetResponse(BaseModel):
    id: int
    name: str
    vlan: int
    classification: str
    network: str
    subnetMaskBits: int
    gateway: Optional[str] = None
    # ipam: Mapped[List["IpRecord"]] = relationship(back_populates="subnet")

# Pydantic model for creating subnets
class SubnetCreate(BaseModel):
    name: str
    vlan: int
    classification: str
    network: str
    subnetMaskBits: int
    gateway: Optional[str] = None

class SubnetUpdateGateway(BaseModel):
    gateway: Optional[str] = None
