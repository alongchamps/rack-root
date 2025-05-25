from pydantic import BaseModel
from typing import Optional

class SubnetResponseOnly(BaseModel):
    id: int
    name: str
    vlan: int
    classification: str
    network: str
    subnetMaskBits: int

class SubnetCreate(BaseModel):
    name: str
    vlan: int
    classification: str
    network: str
    subnetMaskBits: int

# begin classes that have relations to other models
from .validation_dhcpRange import DhcpResponseOnly
from .validation_iprecord import IpRecordOnly

class SubnetResponse(BaseModel):
    id: int
    name: str
    vlan: int
    classification: str
    network: str
    subnetMaskBits: int
    ipam: Optional[list[IpRecordOnly]] = None
    dhcpRange: Optional[list[DhcpResponseOnly]] = None
