# src/infrastructure/models/pod_model.py  (gợi ý tách file model riêng)
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from infrastructure.databases.base import Base
from sqlalchemy.orm import relationship
class PodModel(Base):
    __tablename__ = "pods"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)  # đổi tên cột
    price = Column(Numeric(10, 2), nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    bookings = relationship("BookingModel", back_populates="pod")
