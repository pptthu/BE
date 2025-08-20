from src.infrastructure.models.booking_model import Booking
from src.infrastructure.repositories.base import BaseRepository
from datetime import datetime
from typing import List
class BookingRepository(BaseRepository[Booking]):
    def __init__(self): super().__init__(Booking)
    def list_by_user(self, user_id:int)->List[Booking]:
        return Booking.query.filter_by(user_id=user_id).order_by(Booking.created_at.desc()).all()
    def overlaps(self, pod_id:int, start:datetime, end:datetime)->List[Booking]:
        return (Booking.query.filter_by(pod_id=pod_id)
                .filter(Booking.end_time > start, Booking.start_time < end).all())
    def list_in_day(self, start_dt:datetime, end_dt:datetime)->List[Booking]:
        return (Booking.query.filter(Booking.start_time >= start_dt, Booking.start_time <= end_dt).all())
