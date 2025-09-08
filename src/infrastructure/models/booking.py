from __future__ import annotations
from sqlalchemy import Column, Integer, DateTime, String, Numeric, ForeignKey, func
from sqlalchemy.orm import relationship
from .base import Base

class Booking(Base):
    __tablename__ = "Bookings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    pod_id = Column(Integer, ForeignKey("PODs.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False)  # PENDING/CONFIRMED/CHECKED_IN/COMPLETED
    created_at = Column(DateTime, nullable=False, server_default=func.getdate())
    updated_at = Column(DateTime, nullable=False, server_default=func.getdate(), onupdate=func.getdate())

    user = relationship("User")
    pod = relationship("POD")
