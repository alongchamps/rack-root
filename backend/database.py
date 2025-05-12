# Import necessary modules and classes
from datetime import datetime
from sqlmodel import create_engine, Field, Relationship, Session, SQLModel
from typing import Optional
import os

# Database setup
# look for DATABASE_URL being set by pytest
sqlite_url = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres-fastapi@localhost:5432/postgres")
engine = create_engine(sqlite_url, echo=True)

class DeviceType(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    name: str = Field(index=True)
    items: list["Item"] | None = Relationship(back_populates="deviceType")

class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    name: str = Field(index=True)
    description: Optional[str]
    serialNumber: Optional[str]
    notes: Optional[str]
    purchaseDate: Optional[str]
    warrantyExpiration: Optional[str]
    deviceTypeId: int | None = Field(default=None, foreign_key="devicetype.id")
    deviceType: Optional[DeviceType] | None = Relationship(back_populates="items")

class Subnet(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    name: str = Field(index=True)
    vlan: int
    classification: str
    network: str
    subnetMaskBits: int
    ipam: list["IpRecord"] | None = Relationship(back_populates="subnet")
    dhcpRange: list["DhcpRange"] | None = Relationship(back_populates="subnet")
    dhcpRangeId: int | None = Field(default=None, foreign_key="dhcprange.id")

class IpRecord(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    status: str
    ipAddress: str
    subnetId: int | None = Field(default=None, foreign_key="subnet.id")
    subnet: Optional[Subnet] | None = Relationship(back_populates="ipam")
    dhcpRangeId: int | None = Field(default=None, foreign_key="dhcprange.id")

class DhcpRange(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    subnetId: int | None = Field(default=None, foreign_key="subnet.id")
    subnet: Optional[Subnet] | None = Relationship(back_populates="dhcpRange")
    name: str
    description: Optional[str]
    startIp: str
    endIp: str

# When the nonproduction test database is in use, drop everything to effectively reset it
if( sqlite_url.find("localhost:5555", 0) > -1):
    SQLModel.metadata.drop_all(engine)

# Create tables
SQLModel.metadata.create_all(engine)

# Dependency to get the database session
def getDb():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
