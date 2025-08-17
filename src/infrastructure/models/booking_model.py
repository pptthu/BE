from sqlalchemy import Column, Integer, DateTime, Numeric, String, ForeignKey, func
from sqlalchemy.orm import relationship
from src.infrastructure.databases.mssql import Base

class BookingModel(Base):
    __tablename__ = "Bookings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    pod_id = Column(Integer, ForeignKey("PODs.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.getdate())
    updated_at = Column(DateTime, nullable=False, server_default=func.getdate())

    pod = relationship("PODModel", back_populates="bookings")
    user = relationship("UserModel", back_populates="bookings")
