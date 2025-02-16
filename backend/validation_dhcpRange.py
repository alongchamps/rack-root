from sqlmodel import SQLModel
from typing import Optional

class DhcpResponse(SQLModel):
    id: int
    name: str
    description: Optional[str] = None

class DhcpCreate(SQLModel):
    name: str
    description: Optional[str] = None
    start: str
    end: str
