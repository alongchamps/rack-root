# Import necessary modules and classes
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from typing import Optional
import os

# Database setup
# look for DATABASE_URL being set by pytest
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./backend/production.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()

# Database model
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

# Pydantic model for request data
class ItemCreate(BaseModel):
    name: str
    description: str

# Pydantic model for updating a record
class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

# Pydantic model for response data
class ItemResponse(BaseModel):
    id: int
    name: str
    description: str

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
