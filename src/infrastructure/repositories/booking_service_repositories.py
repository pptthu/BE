from typing import List
from src.models.booking_service import BookingService
from src.repositories.base import BaseRepository

class BookingServiceRepository(BaseRepository[BookingService]):
    def __init__(self):
        super().__init__(BookingService)

    def list_by_booking(self, booking_id: int) -> List[BookingService]:
        return BookingService.query.filter_by(booking_id=booking_id).all()
