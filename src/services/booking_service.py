from typing import List, Optional
from datetime import datetime
from domain.models.booking import Booking               
from domain.models.ibooking_repository import IBookingRepository

class BookingService:
    def __init__(self, repository: IBookingRepository):
        self.repository = repository

    @staticmethod
    def _is_overlap(a_start: datetime, a_end: datetime, b_start: datetime, b_end: datetime) -> bool:
        return not (b_end <= a_start or b_start >= a_end)

    def _validate_time_range(self, start_time: datetime, end_time: datetime):
        if not isinstance(start_time, datetime) or not isinstance(end_time, datetime):
            raise ValueError("start_time và end_time phải là datetime")
        if end_time <= start_time:
            raise ValueError("end_time phải lớn hơn start_time")

    def create_booking(
        self,
        user_id: int,
        pod_id: int,
        start_time: datetime,
        end_time: datetime,
        status: Optional[str],
        created_at: datetime,
        updated_at: datetime
    ) -> Booking:
        self._validate_time_range(start_time, end_time)
        status = status or "CONFIRMED"

        active_status = {"PENDING", "CONFIRMED", "CHECKED_IN"}
        for b in self.repository.list():
            if b.pod_id == pod_id and b.status in active_status:
                if self._is_overlap(start_time, end_time, b.start_time, b.end_time):
                    raise ValueError("POD đã được đặt trong khoảng thời gian này")

        booking = Booking(
            id=None,
            user_id=user_id,
            pod_id=pod_id,
            start_time=start_time,
            end_time=end_time,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            total_price=None,          # hoặc tính tiền tại đây
        )
        return self.repository.add(booking)

    def get_booking(self, booking_id: int) -> Optional[Booking]:
        return self.repository.get_by_id(booking_id)

    def list_bookings(self) -> List[Booking]:
        return self.repository.list()

    def update_booking(
        self,
        booking_id: int,
        user_id: int,
        pod_id: int,
        start_time: datetime,
        end_time: datetime,
        status: Optional[str],
        created_at: Optional[datetime],
        updated_at: datetime
    ) -> Booking:
        self._validate_time_range(start_time, end_time)
        status = status or "CONFIRMED"

        current = self.repository.get_by_id(booking_id)
        if not current:
            raise ValueError("Booking not found")

        active_status = {"PENDING", "CONFIRMED", "CHECKED_IN"}
        for b in self.repository.list():
            if b.id == booking_id:
                continue
            if b.pod_id == pod_id and b.status in active_status:
                if self._is_overlap(start_time, end_time, b.start_time, b.end_time):
                    raise ValueError("POD đã được đặt trong khoảng thời gian này")

        booking = Booking(
            id=booking_id,
            user_id=user_id,
            pod_id=pod_id,
            start_time=start_time,
            end_time=end_time,
            status=status,
            created_at=current.created_at if created_at is None else created_at,
            updated_at=updated_at,
            total_price=current.total_price,   # giữ nguyên (hoặc tính lại)
        )
        return self.repository.update(booking)

    def delete_booking(self, booking_id: int) -> bool:   # <-- trả bool
        return self.repository.delete(booking_id)
