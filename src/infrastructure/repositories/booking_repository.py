from domain.models.ibooking_repository import IBookingRepository
from domain.models.booking import Booking
from typing import List, Optional
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Config
from sqlalchemy import Column, Integer, String, DateTime,Numeric,ForeignKey
from infrastructure.databases import Base
from decimal import Decimal






load_dotenv()


class BookingRepository(IBookingRepository):
    """
    Repository lưu RAM, tương tự TodoRepository cũ.
    Dùng cho demo/dev. Sau này có DB thì thay bằng bản dùng Session.
    """
    def __init__(self):
        self._bookings: List[Booking] = []
        self._id_counter: int = 1

    def add(self, booking: Booking) -> Booking:
        booking.id = self._id_counter
        self._id_counter += 1
        self._bookings.append(booking)
        return booking

    def get_by_id(self, booking_id: int) -> Optional[Booking]:
        for b in self._bookings:
            if b.id == booking_id:
                return b
        return None

    def list(self) -> List[Booking]:
        return list(self._bookings)

    def update(self, booking: Booking) -> Booking:
        for idx, b in enumerate(self._bookings):
            if b.id == booking.id:
                self._bookings[idx] = booking
                return booking
        raise ValueError("Booking not found")

    def delete(self, booking_id: int) -> bool:
        before = len(self._bookings)
        self._bookings = [b for b in self._bookings if b.id != booking_id]
        return len(self._bookings) < before


class BookingModel(Base):
    """
    ORM mapping tới bảng 'bookings' trong DB.
    Không dùng trực tiếp trong memory repo ở trên.
    Sau này nếu anh viết SqlAlchemyBookingRepository, hãy map giữa
    Booking (domain) <-> BookingModel (ORM) tại đó.
    """
    __tablename__ = "bookings"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    pod_id = Column(Integer, ForeignKey("pods.id"), nullable=False, index=True)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False, index=True)
    status = Column(String(50), nullable=False, default="CONFIRMED", index=True)
    total_price = Column(Numeric(10, 2))  # dùng Numeric để biểu diễn tiền
    created_at = Column(DateTime)
    updated_at = Column(DateTime)



