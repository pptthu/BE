from sqlalchemy.orm import Session
from ..infrastructure.repositories.booking_repository import BookingRepository
from ..infrastructure.models.base import now_utc
from ..domain.exceptions import AppError

class StaffService:
    def __init__(self, session: Session):
        self.db = session
        self.repo = BookingRepository(session)

    def list_bookings(self):
        from ..infrastructure.models.booking import Booking
        items = self.db.query(Booking).order_by(Booking.id.desc()).all()
        return [self._to_dict(b) for b in items]

    def checkin(self, booking_id: int):
        b = self.repo.get(booking_id)
        if not b:
            raise AppError("Booking not found", 404)
        b.status = "CHECKED_IN"
        b.updated_at = now_utc()
        self.db.commit()
        return self._to_dict(b)

    def checkout(self, booking_id: int):
        b = self.repo.get(booking_id)
        if not b:
            raise AppError("Booking not found", 404)
        b.status = "CHECKED_OUT"
        b.updated_at = now_utc()
        pod = self.repo.get_pod(b.pod_id)
        if pod:
            pod.status = "AVAILABLE"
        self.db.commit()
        return self._to_dict(b)

    def _to_dict(self, b):
        return {
            "id": b.id, "user_id": b.user_id, "pod_id": b.pod_id,
            "start_time": b.start_time.isoformat() if b.start_time else None,
            "end_time": b.end_time.isoformat() if b.end_time else None,
            "total_price": float(b.total_price), "status": b.status, "paid": b.paid,
            "created_at": b.created_at.isoformat() if b.created_at else None,
            "updated_at": b.updated_at.isoformat() if b.updated_at else None,
        }
