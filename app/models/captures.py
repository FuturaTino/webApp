from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base

class Capture(Base):
    __tablename__ = "captures"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(255), index=True)
    slug = Column(String(255), index=True)
    title = Column(String(255), index=True)
    work_type = Column(String(255), index=True)
    date = Column(String(255), index=True)
    source_url = Column(String(255), index=True)
    image_url = Column(String(255), index=True)
    result_url = Column(String(255), index=True)
    latest_run_status = Column(String(255), index=True)
    latest_run_current_stage = Column(String(255), index=True)
    
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="captures")
