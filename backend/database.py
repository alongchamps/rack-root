# Import necessary modules and classes
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import sessionmaker, relationship, mapped_column
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
    purchaseDate = Column(DateTime)
    warrantyExpiration = Column(DateTime)
    notes = Column(String)

    deviceTypeId = mapped_column(ForeignKey("deviceTypes.id"), nullable=True)
    deviceType = relationship("DeviceType", foreign_keys="Item.deviceTypeId")

class DeviceType(Base):
    __tablename__ = "deviceTypes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Subnet(Base):
    __tablename__ = "subnets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    vlan = Column(Integer)
    classification = Column(String)
    network = Column(String)
    subnetMaskBits = Column(Integer)
    gateway = Column(String)
    # ipam = relationship("IpRecord", back_populates="subnet")

class IpRecord(Base):
    __tablename__ = "iprecords"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String)
    ipaddress = Column(String)
    # subnet_id = mapped_column(ForeignKey("subnets.id"))
    # subnet = relationship("Subnet", back_populates="ipam")

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
