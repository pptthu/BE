from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from src.infrastructure.databases.mssql import Base

class LocationModel(Base):
    __tablename__ = "Locations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.getdate())
    updated_at = Column(DateTime, nullable=False, server_default=func.getdate())

    # cặp back_populates khớp với PODModel.location
    pods = relationship("PODModel", back_populates="location")
