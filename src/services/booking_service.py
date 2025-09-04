import datetime as dt
from sqlalchemy.orm import Session
from ..infrastructure.repositories.booking_repository import BookingRepository
from ..infrastructure.models.booking import Booking
from ..infrastructure.models.base import now_utc
from ..domain.exceptions import AppError

<<<<<<< HEAD
def _parse_iso(x):
    try:
        return dt.datetime.fromisoformat(x.replace("Z", ""))
    except Exception:
        return None
=======
from infrastructure.repositories.booking_repository import BookingRepository
from infrastructure.models.booking_model import BookingModel

def calc_price(pod: POD, start: datetime, end: datetime, services: list) -> float:
    """
    Tính tổng tiền = (giờ thuê * giá POD/giờ) + (cộng các dịch vụ)
    - services: [{ "service_id": int, "quantity": int }, ...]
    """
    hours = (end - start).total_seconds() / 3600.0
    hours = max(hours, 0.0)
    total = float(pod.price) * float(hours)
>>>>>>> origin/main

class BookingService:
    def __init__(self, session: Session):
        self.db = session
        self.repo = BookingRepository(session)

    def _has_overlap(self, pod_id: int, start: dt.datetime, end: dt.datetime) -> bool:
        return self.repo.has_overlap(pod_id=pod_id, start=start, end=end)

    def create_booking(self, user_id: int, pod_id: int, start_time: str, end_time: str):
        pod = self.repo.get_pod(pod_id)
        if not pod:
            raise AppError("POD not found", 404)

        start = _parse_iso(start_time)
        end = _parse_iso(end_time)
        if not start or not end or end <= start:
            raise AppError("Invalid start_time/end_time", 400)

        if self._has_overlap(pod_id, start, end):
            raise AppError("Pod is not available in the selected time range", 400)

        b = Booking(
            user_id=user_id,
            pod_id=pod.id,
            start_time=start,
            end_time=end,
            total_price=pod.price,
            status="PENDING",
            created_at=now_utc(),
            updated_at=now_utc()
        )
<<<<<<< HEAD
        self.repo.add(b)
        self.db.commit()
        return self._to_dict(b)

    def get(self, booking_id: int, owner_id: int):
        b = self.repo.get(booking_id)
        if not b or b.user_id != owner_id:
            return None
        return self._to_dict(b)

    def list_my_bookings(self, user_id: int):
        items = self.repo.list_by_user(user_id)
        return [self._to_dict(b) for b in items]

    def confirm_payment(self, user_id: int, booking_id: int):
        b = self.repo.get(booking_id)
        if not b or b.user_id != user_id:
            raise AppError("Booking not found", 404)
        if b.paid:
            return self._to_dict(b)
        b.paid = True
        b.status = "CONFIRMED"
        b.updated_at = now_utc()
        self.db.commit()
        return self._to_dict(b)

    def _to_dict(self, b: Booking):
        return {
            "id": b.id,
            "user_id": b.user_id,
            "pod_id": b.pod_id,
            "start_time": b.start_time.isoformat() if b.start_time else None,
            "end_time": b.end_time.isoformat() if b.end_time else None,
            "total_price": float(b.total_price),
            "status": b.status,
            "paid": b.paid,
            "created_at": b.created_at.isoformat() if b.created_at else None,
            "updated_at": b.updated_at.isoformat() if b.updated_at else None,
        }
=======

class BookingService:
    def __init__(self, repo: BookingRepository):
        self.repo = repo

    def list_bookings(self, date: str = None):
        """
        Lấy danh sách booking cho nhân viên trong ngày.
        """
        return self.repo.list_for_staff(date)

    def check_in(self, booking_id: int, at_time: datetime = None):
        """
        Xác nhận check-in: chỉ hợp lệ khi trạng thái là PENDING hoặc CONFIRMED.
        """
        booking = self.repo.get_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found")

        if booking.status not in ["PENDING", "CONFIRMED"]:
            raise ValueError("Booking not in valid state for check-in")

        booking.status = "CHECKED_IN"
        booking.updated_at = at_time or datetime.utcnow()
        return self.repo.update(booking)

    def check_out(self, booking_id: int, at_time: datetime = None):
        """
        Xác nhận check-out: chỉ hợp lệ khi trạng thái là CHECKED_IN.
        """
        booking = self.repo.get_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found")

        if booking.status != "CHECKED_IN":
            raise ValueError("Booking not in valid state for check-out")

        booking.status = "CHECKED_OUT"
        booking.updated_at = at_time or datetime.utcnow()

        # (Tùy chọn) tính tiền
        if booking.start_time and booking.end_time and booking.pod:
            duration = (booking.end_time - booking.start_time).seconds / 3600
            booking.total_price = float(duration) * float(booking.pod.price)

        return self.repo.update(booking)
>>>>>>> origin/main
