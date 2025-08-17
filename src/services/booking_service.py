from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, List
from src.infrastructure.models.booking_model import BookingModel
from src.infrastructure.models.pod_model import PODModel

class BookingService:
    @staticmethod
    def _to_dt(value: str) -> datetime:
        try:
            return datetime.fromisoformat(str(value))
        except Exception:
            raise ValueError("Invalid datetime format. Use ISO 8601, e.g. 2025-08-17T09:00:00")

    @staticmethod
    def calc_total_price(pod_price: Decimal, start_time: datetime, end_time: datetime) -> Decimal:
        if end_time <= start_time:
            raise ValueError("end_time must be greater than start_time")
        seconds = Decimal((end_time - start_time).total_seconds())
        hours = (seconds / Decimal(3600)).quantize(Decimal("0.0001"))
        return (pod_price * hours).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @staticmethod
    def create_booking(session, user_id: int, pod_id: int, start_iso: str, end_iso: str, status: str = "pending") -> BookingModel:
        start_time = BookingService._to_dt(start_iso)
        end_time = BookingService._to_dt(end_iso)

        pod: Optional[PODModel] = session.get(PODModel, pod_id)
        if not pod:
            raise LookupError("POD not found")

        overlap = session.execute(
            """SELECT 1 FROM Bookings WITH (NOLOCK)
               WHERE pod_id = :pid AND NOT (:end <= start_time OR :start >= end_time)""",
            {"pid": pod.id, "start": start_time, "end": end_time}
        ).first()
        if overlap:
            raise ValueError("Time range overlaps an existing booking.")

        total_price = BookingService.calc_total_price(Decimal(pod.price), start_time, end_time)

        booking = BookingModel(
            user_id=user_id, pod_id=pod.id,
            start_time=start_time, end_time=end_time,
            total_price=total_price, status=status,
        )
        session.add(booking); session.commit(); session.refresh(booking)
        return booking

    @staticmethod
    def confirm_booking(session, booking_id: int) -> BookingModel:
        booking = session.get(BookingModel, booking_id)
        if not booking: raise LookupError("Booking not found")
        booking.status = "confirmed"; session.commit(); session.refresh(booking); return booking

    @staticmethod
    def cancel_booking(session, booking_id: int) -> BookingModel:
        booking = session.get(BookingModel, booking_id)
        if not booking: raise LookupError("Booking not found")
        booking.status = "canceled"; session.commit(); session.refresh(booking); return booking

    @staticmethod
    def list_for_user(session, user_id: int) -> List[BookingModel]:
        return (session.query(BookingModel)
                .filter(BookingModel.user_id == user_id)
                .order_by(BookingModel.id.desc()).all())

    @staticmethod
    def list_all(session) -> List[BookingModel]:
        return session.query(BookingModel).order_by(BookingModel.id.desc()).all()
