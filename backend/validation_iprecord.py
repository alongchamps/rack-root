from pydantic import BaseModel
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from .database import Subnet

# pydantic model for creating IP records
class IpRecordResponse(BaseModel):
    id: int
    subnet_id: int
    item_id: Optional[int]
    status: str
    ipaddress: str
    # subnet_id: Mapped[int] = mapped_column(ForeignKey("subnets.id"))
    # subnet: Mapped["Subnet"] = relationship(back_populates="ipam")

# class Parent(Base):
#     __tablename__ = "parent_table"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     children: Mapped[List["Child"]] = relationship(back_populates="parent")
#     ipam: Mapped[List["IpRecord"]] = relationship(back_populates="subnet")


# class Child(Base):
#     __tablename__ = "child_table"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table.id"))
#     parent: Mapped["Parent"] = relationship(back_populates="children")
