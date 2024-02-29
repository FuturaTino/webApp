from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), index=True)
    username = Column(String(255), unique=True, index=True)
    is_active = Column(Boolean, default=True)
    password  = Column(String(255), index=True, nullable=False)
    # profile_photo = Column(String)
    captures = relationship("Capture", back_populates="owner", cascade="all, delete")
