# Import necessary modules and classes
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel
from datetime import date
from typing import Optional
import os

# Database setup
# look for DATABASE_URL being set by pytest
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./backend/production.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    serialNumber = Column(String)
    purchaseDate = Column(Date)
    warrantyExpiration = Column(Date)
    notes = Column(String)

# Pydantic model for creating an item
class ItemCreate(BaseModel):
    name: str
    description: str
    serialNumber: Optional[str] =  None
    purchaseDate: Optional[date] =  None
    warrantyExpiration: Optional[date] =  None
    notes: Optional[str] =  None

# Pydantic model for updating an item
class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    serialNumber: Optional[str] =  None
    purchaseDate: Optional[date] =  None
    warrantyExpiration: Optional[date] =  None
    notes: Optional[str] =  None

# Pydantic model for responding with an item
class ItemResponse(BaseModel):
    id: int
    name: str
    description: str
    serialNumber: str
    purchaseDate: date
    warrantyExpiration: date
    notes: str

class DeviceType(Base):
    __tablename__ = "deviceTypes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# Pydantic model for returning device types
class DeviceTypeResponse(BaseModel):
    id: int
    name: str

# Pydantic model for creating device types
class DeviceTypeCreate(BaseModel):
    name: str

# Pydantic model for updating a device
class DeviceTypeUpdate(BaseModel):
    name: Optional[str] = None

# assocation table for items and device types
class ItemDeviceTypeAssociation(Base):
    __tablename__ = "ItemDevTypeAssoc"

    id = Column(Integer, primary_key=True)
    itemId = Column(Integer, ForeignKey('items.id'))
    deviceTypeId = Column(Integer, ForeignKey('deviceTypes.id'))
    item = relationship("Item", backref="deviceTypes")
    deviceType = relationship("DeviceType", backref="items")

# When the nonproduction test database is in use, drop everything to effectively reset it
if( DATABASE_URL.find("nonproduction.db", 0) > -1 ):
    Base.metadata.drop_all(bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
