from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from infrastructure.databases.base import Base

class LocationModel(Base):
    __tablename__ = 'locations'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    address = Column(String(255), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
