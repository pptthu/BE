from sqlalchemy.orm import Session
from ..models.booking import Booking
from ..models.pod import POD

class BookingRepository:
    def __init__(self, session: Session):
        self.db = session

    def add(self, booking: Booking):
        self.db.add(booking)
        self.db.flush()
        return booking

    def get(self, booking_id: int):
        return self.db.query(Booking).filter(Booking.id == booking_id).first()

    def list_by_user(self, user_id: int):
        return (self.db.query(Booking)
                .filter(Booking.user_id == user_id)
                .order_by(Booking.id.desc())
                .all())

    def get_pod(self, pod_id: int):
        return self.db.query(POD).filter(POD.id == pod_id).first()

    def has_overlap(self, pod_id: int, start, end) -> bool:
        q = self.db.query(Booking).filter(
            Booking.pod_id == pod_id,
            Booking.status.in_(["PENDING", "CONFIRMED", "CHECKED_IN"]),
            Booking.start_time < end,
            Booking.end_time > start
        )
        return self.db.query(q.exists()).scalar()