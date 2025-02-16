from sqlmodel import SQLModel
from typing import Optional

class DhcpResponse(SQLModel):
    id: int
    name: str
    description: Optional[str] = None
    startIp: str
    endIp: str

class DhcpCreate(SQLModel):
    name: str
    description: Optional[str] = None
    startIp: str
    endIp: str
