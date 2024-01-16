from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from ..db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")
    captures = relationship("Capture", back_populates="owner", cascade="all, delete")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

class Capture(Base):
    __tablename__ = "captures"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, index=True)
    slug = Column(String, index=True)
    title = Column(String, index=True)
    work_type = Column(String, index=True)
    date = Column(String, index=True)
    source_url = Column(String, index=True)
    result_url = Column(String, index=True)
    latest_run_status = Column(String, index=True)
    latest_run_current_stage = Column(String, index=True)
    
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="captures")
