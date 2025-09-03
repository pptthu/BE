from datetime import datetime
from src.infrastructure.models.pod_model import POD
from src.infrastructure.models.service_model import Service
from src.infrastructure.models.booking_service_model import BookingService
from src.infrastructure.databases.extensions import db
from src.dependency_container import booking_repo

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

    for item in services or []:
        svc = Service.query.get(item.get("service_id"))
        if not svc:
            continue
        qty = int(item.get("quantity", 1))
        total += float(svc.price) * qty

    return round(total, 2)

def ensure_not_overlap(pod_id: int, start: datetime, end: datetime) -> bool:
    """
    Kiểm tra khoảng thời gian không bị đè lên các booking 'đang hoạt động':
    pending | confirmed | checked_in
    """
    conflicts = booking_repo.overlaps(pod_id, start, end)
    return all(b.status not in ("pending", "confirmed", "checked_in") for b in conflicts)

def attach_services(booking_id: int, services: list):
    """
    Gắn các dịch vụ vào booking (bảng nối Booking_Services).
    - services: [{ "service_id": int, "quantity": int }, ...]
    """
    for item in services or []:
        svc = Service.query.get(item.get("service_id"))
        if not svc:
            continue
        qty = int(item.get("quantity", 1))
        db.session.add(
            BookingService(booking_id=booking_id, service_id=svc.id, quantity=qty)
        )

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