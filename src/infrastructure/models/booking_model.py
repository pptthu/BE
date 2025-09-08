# src/infrastructure/models/booking_model.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from infrastructure.databases.base import Base
from sqlalchemy.orm import relationship

class BookingModel(Base):
    __tablename__ = "bookings"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    pod_id = Column(Integer, ForeignKey("pods.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    total_price = Column(Numeric(10, 2), nullable=True)
    status = Column(String, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # Dùng module-qualified path để chắc chắn tránh trùng tên class
    user = relationship("infrastructure.models.users_model.UserModel", back_populates="bookings")
    pod  = relationship("infrastructure.models.pods_model.PodModel",  back_populates="bookings")
