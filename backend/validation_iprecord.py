from sqlmodel import SQLModel
from typing import Optional
from .validation_subnet import SubnetResponse

# class IpRecordCreate(SQLModel):
#     status: str
#     ipAddress: str
#     subnetId: int

class IpRecordResponse(SQLModel):
    id: int
    status: str
    ipAddress: str
    subnetId: Optional[int]
    subnet: Optional[SubnetResponse]

class IpRecordGateway(SQLModel):
    gateway: str
