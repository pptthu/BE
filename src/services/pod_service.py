from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base

class PodModel(Base):
    __tablename__ = 'pods'

    id = Column(Integer, primary_key=True)
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default="active")

    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    location = relationship("LocationModel", backref="pods")

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
