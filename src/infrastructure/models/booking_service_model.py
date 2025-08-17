from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional

from src.infrastructure.models.booking_model import BookingModel
from src.infrastructure.models.pod_model import PODModel

class BookingService:
    @staticmethod
    def calc_total_price(pod_price: Decimal, start_time: datetime, end_time: datetime) -> Decimal:
        """
        Tính tổng tiền theo giờ, làm tròn 2 chữ số thập phân.
        """
        if end_time <= start_time:
            raise ValueError("end_time must be greater than start_time")
        seconds = Decimal((end_time - start_time).total_seconds())
        hours = (seconds / Decimal(3600)).quantize(Decimal("0.0001"))
        total = (pod_price * hours).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return total

    @staticmethod
    def create_booking(session, user_id: int, pod_id: int, start_iso: str, end_iso: str, status: str = "pending") -> BookingModel:
        """
        Tạo booking mới, tự tính total_price từ giá POD.
        """
        try:
            start_time = datetime.fromisoformat(start_iso)
            end_time = datetime.fromisoformat(end_iso)
        except Exception:
            raise ValueError("Invalid datetime format. Use ISO 8601, e.g. 2025-08-17T09:00:00")

        pod: Optional[PODModel] = session.get(PODModel, pod_id)
        if not pod:
            raise LookupError("POD not found")

        total_price = BookingService.calc_total_price(Decimal(pod.price), start_time, end_time)

        booking = BookingModel(
            user_id=user_id,
            pod_id=pod.id,
            start_time=start_time,
            end_time=end_time,
            total_price=total_price,
            status=status,
        )
        session.add(booking)
        session.commit()
        session.refresh(booking)
        return booking

    @staticmethod
    def confirm_booking(session, booking_id: int) -> BookingModel:
        """
        Đổi trạng thái booking sang 'confirmed'.
        """
        booking = session.get(BookingModel, booking_id)
        if not booking:
            raise LookupError("Booking not found")
        booking.status = "confirmed"
        session.commit()
        session.refresh(booking)
        return booking
