from datetime import datetime
from infrastructure.models.booking_model import BookingModel

class BookingService:
    def __init__(self, repo):
        self.repo = repo

    def list_bookings(self):
        return self.repo.list_bookings()

    def check_in(self, booking_id: int, at_time: datetime | None = None):
        b: BookingModel = self.repo.get_by_id(booking_id)
        if not b:
            return None
        # Cho phép check-in khi còn CONFIRMED/PENDING
        if b.status not in ("CONFIRMED", "PENDING"):
            raise ValueError("Chỉ được check-in khi booking ở trạng thái CONFIRMED/PENDING")
        b.status = "CHECKED_IN"
        b.updated_at = at_time or datetime.now()
        return self.repo.save(b)

    def check_out(self, booking_id: int, at_time: datetime | None = None):
        b: BookingModel = self.repo.get_by_id(booking_id)
        if not b:
            return None
        if b.status != "CHECKED_IN":
            raise ValueError("Chỉ được check-out khi booking đang ở trạng thái CHECKED_IN")
        b.status = "CHECKED_OUT"
        b.updated_at = at_time or datetime.now()
        return self.repo.save(b)
