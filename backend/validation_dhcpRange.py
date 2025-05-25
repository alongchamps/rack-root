from pydantic import BaseModel
from typing import Optional

class DhcpResponseOnly(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    startIp: str
    endIp: str

# begin classes that have relations to other models
from .validation_iprecord import IpRecordOnly
from .validation_subnet import SubnetResponseOnly

class DhcpResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    startIp: str
    endIp: str
    subnet: SubnetResponseOnly
    ipRecord: list[IpRecordOnly]

class DhcpCreate(BaseModel):
    name: str
    description: Optional[str] = None
    startIp: str
    endIp: str
