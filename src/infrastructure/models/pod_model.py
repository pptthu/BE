from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, func
from sqlalchemy.orm import relationship
from src.infrastructure.databases.mssql import Base

class PODModel(Base):
    __tablename__ = "PODs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False)
    location_id = Column(Integer, ForeignKey("Locations.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.getdate())
    updated_at = Column(DateTime, nullable=False, server_default=func.getdate())

    # THUỘC TÍNH NÀY LÀ BẮT BUỘC để khớp với LocationModel.pods
    location = relationship("LocationModel", back_populates="pods")

    # cho quan hệ với BookingModel
    bookings = relationship("BookingModel", back_populates="pod")
