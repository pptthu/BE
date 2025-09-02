from sqlalchemy import Column, Integer, String, DateTime
from infrastructure.databases.base import Base

class LocationModel(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    address = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
