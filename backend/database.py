# Import necessary modules and classes
from datetime import datetime
from sqlalchemy import Column, create_engine, DDL, event, ForeignKey, Index, MetaData

from sqlalchemy.orm import configure_mappers, DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType

from typing import List, Optional
import os

# Database setup
# look for DATABASE_URL being set by pytest or other env vars
sqlite_url = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres-fastapi@localhost:5432/postgres")
engine = create_engine(sqlite_url, pool_size=20, max_overflow=10, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    pass

# call this after the Base class is defined, but before other classes, 
# in order to make them searchable
make_searchable(Base.metadata)

class DeviceType(Base):
    __tablename__ = "devicetype"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    name: Mapped[str]
    item: Mapped[Optional[List["Item"]]] = relationship(back_populates="deviceType", lazy="joined")

    class Config:
        orm_mode = True

class Item(Base):

    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    # serialNumber is renamed for the database since the search vectors work against lowercase names
    # and serialNumber here is in camel case. I chose not to rename it here since I would need to rewrite
    # any instance where serialNumber is used, everywhere from the frontend to the backend.
    serialNumber: Mapped[Optional[str]] = mapped_column(name="serial_number")
    notes: Mapped[Optional[str]]
    purchaseDate: Mapped[Optional[datetime]]
    warrantyExpiration: Mapped[Optional[datetime]]
    deviceTypeId: Mapped[int] = mapped_column(ForeignKey("devicetype.id", ondelete="CASCADE"))
    deviceType: Mapped["DeviceType"] = relationship(back_populates="item", foreign_keys=[deviceTypeId], lazy="joined")

    # define a search vector only for the columns name, description, serial_number, and notes
    item_search_vector = Column(TSVectorType("name", "description", "serial_number", "notes"))

    __table_args__ = (
        Index("ix_item_search_vector",
                "item_search_vector",
                postgresql_using="gin"
        ),
    )

    class Config:
        orm_mode = True

class Subnet(Base):
    __tablename__ = "subnet"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str]
    vlan: Mapped[int]
    classification: Mapped[str]
    network: Mapped[str]
    subnetMaskBits: Mapped[int]
    
    # add in 2 fields - IpRecord
    # ipRecordId: Mapped[Optional[List[int]]] = mapped_column(ForeignKey("iprecord.id"))
    # ipRecord: Mapped[Optional[List["IpRecord"]]] = relationship(back_populates="subnet", foreign_keys=[ipRecordId], lazy="joined")
    # ipRecord: Mapped[Optional[List["IpRecord"]]] = relationship(back_populates="subnet", foreign_keys=[ipRecordId], lazy="joined", innerjoin=True)
    ipRecord: Mapped[Optional[List["IpRecord"]]] = relationship(back_populates="subnet", cascade="all, delete-orphan")
    
    # add in 2 fields - DhcpRange
    dhcpRangeId: Mapped[Optional[List[int]]] = mapped_column(ForeignKey("dhcprange.id"))
    # dhcpRange: Mapped[Optional[List["DhcpRange"]]] = relationship(back_populates="subnet", foreign_keys=[dhcpRangeId])

    class Config:
        orm_mode = True

class IpRecord(Base):
    __tablename__ = "iprecord"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    status: Mapped[str]
    ipAddress: Mapped[str]

    # add in 2 fields - Subnet
    subnetId: Mapped[Optional[int]] = mapped_column(ForeignKey("subnet.id", ondelete="CASCADE"))
    # subnet: Mapped[Optional["Subnet"]] = relationship(back_populates="ipRecord", foreign_keys=[subnetId], lazy="joined", innerjoin=True)
    subnet: Mapped["Subnet"] = relationship(back_populates="ipRecord")

    # add in 2 fields - DhcpRange
    dhcpRangeId: Mapped[Optional[int]] = mapped_column(ForeignKey("dhcprange.id"))
    # dhcpRange: Mapped["DhcpRange"] = relationship(back_populates="ipRecord", foreign_keys=[dhcpRangeId])
    
    class Config:
        orm_mode = True

class DhcpRange(Base):
    __tablename__ = "dhcprange"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str]
    description: Mapped[Optional[str]]
    startIp: Mapped[str]
    endIp:Mapped[str]

    # add in 2 fields - Subnet
    subnetId: Mapped[int] = mapped_column(ForeignKey("subnet.id", ondelete="CASCADE"))
    # subnet: Mapped["Subnet"] = relationship(back_populates="dhcpRange", foreign_keys=[subnetId])

    # add in 2 fields - IpRecord
    ipRecordId: Mapped[Optional[List[int]]] = mapped_column(ForeignKey("iprecord.id", ondelete="CASCADE"))
    # ipRecord: Mapped[List["IpRecord"]] = relationship(back_populates="dhcpRange", foreign_keys=[ipRecordId])
    
    class Config:
        orm_mode = True



# When the nonproduction test database is in use, drop everything to effectively empty it
if( sqlite_url.find("localhost:5555", 0) > -1):
    m = MetaData()
    m.reflect(engine)
    m.drop_all(engine)
    Base.metadata.drop_all(engine)

# Create tables
# make_searchable(Base.metadata)
configure_mappers()
Base.metadata.create_all(engine)

# event listeners for search triggers
# event.listen(Base.metadata, "after_create", Item.itemSearchTrigger.execute_if(dialect="postgresql"))

# Dependency to get the database session
def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Notes
# .join syntax for database queries
# .join(<remote object type>, <localrecord.remoteId> == <remote object type>.id)
# example: .join(Subnet, IpRecord.subnetId == Subnet.id)
