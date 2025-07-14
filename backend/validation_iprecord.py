from pydantic import BaseModel
from typing import Optional

class IpRecordOnly(BaseModel):
    id: int
    status: str
    ipAddress: str

# begin classes that have relations to other models
from .validation_dhcpRange import DhcpResponseOnly
from .validation_subnet import SubnetResponseOnly

class IpRecordResponse(BaseModel):
    id: int
    status: str
    ipAddress: str
    subnet: Optional[SubnetResponseOnly]
    dhcpRange: Optional[DhcpResponseOnly] = None

class IpRecordGateway(BaseModel):
    ipAddress: str
