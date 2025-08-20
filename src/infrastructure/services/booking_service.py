# src/infrastructure/services/booking_service.py
from datetime import datetime
from decimal import Decimal
from src.models.booking_model import Booking
from src.infrastructure.repositories.booking_repository import BookingRepository

class BookingService:
    def __init__(self, repo: BookingRepository): self.repo = repo

    def create_booking(self, db, user_id: int, pod_id: int, start: datetime, end: datetime, amount: Decimal):
        booking = Booking(user_id=user_id, pod_id=pod_id, start_time=start, end_time=end, amount=amount, status="pending")
        return self.repo.create(booking)

    def get(self, booking_id: int): return self.repo.get(booking_id)

    def list_my_bookings(self, user_id: int): return self.repo.list_by_user(user_id)
