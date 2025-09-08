from __future__ import annotations
from typing import Any, Dict, List, Optional
from datetime import datetime

from ..infrastructure.repositories.booking_repository import BookingRepository

def _parse_dt(v) -> datetime:
    if isinstance(v, datetime):
        return v
    return datetime.fromisoformat(str(v).replace(" ", "T"))

class BookingService:
    def __init__(self, repo: BookingRepository):
        self.repo = repo

    # CUSTOMER
    def create_booking(self, current_user, data: Dict[str, Any]):
        uid = getattr(current_user, "id", None) or data.get("user_id")
        if not uid:
            raise ValueError("Missing current user")
        pod_id = int(data.get("pod_id") or data.get("podId"))
        start_time = _parse_dt(data.get("start_time") or data.get("start") or data.get("startTime"))
        end_time   = _parse_dt(data.get("end_time")   or data.get("end")   or data.get("endTime"))
        status     = data.get("status") or "PENDING"
        total_price = data.get("total_price")

        if not self.repo.get_pod(pod_id):
            raise ValueError("POD not found")

        if self.repo.has_overlap(pod_id, start_time=start_time, end_time=end_time):
            raise ValueError("Time range overlaps existing booking")

        return self.repo.add(
            user_id=uid, pod_id=pod_id,
            start_time=start_time, end_time=end_time,
            status=status, total_price=total_price,
        )

    def my_bookings(self, current_user) -> List:
        uid = getattr(current_user, "id", None)
        if not uid:
            raise ValueError("Missing current user")
        return self.repo.list_by_user(uid)

    # STAFF/ADMIN
    def todays_bookings_for_staff(self):
        return self.repo.list_for_staff_today()

    def confirm_payment(self, booking_id: int):
        return self.repo.confirm_payment(booking_id)

    def checkin(self, booking_id: int):
        return self.repo.checkin(booking_id)

    def checkout(self, booking_id: int):
        return self.repo.checkout(booking_id)
