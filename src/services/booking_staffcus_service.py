
# src/services/booking_service.py
from __future__ import annotations
from datetime import datetime
from typing import Optional, Tuple, List

# booking_repo: infrastructure.repositories.booking_repository.BookingRepository
# pod_repo: infrastructure.repositories.pod_cus_repository.PodRepository (in-memory demo)
# user_repo: infrastructure.repositories.user_cus_repository.UserRepository (in-memory demo)
class BookingService:
    def __init__(self, booking_repo=None, pod_repo=None, user_repo=None):
        self.booking_repo = booking_repo
        self.pod_repo = pod_repo
        self.user_repo = user_repo

    # ---------- CUSTOMER ----------
    def list_pods(self, page: int, limit: int, location_id: Optional[int]):
        # in-memory repo demo đã có sẵn paging + filter
        return self.pod_repo.list_pods(page, limit, location_id)

    def create_booking_for_customer(
        self,
        user_id: int,
        pod_id: int,
        start_time: datetime,
        end_time: datetime,
    ):
        if start_time >= end_time:
            raise ValueError("start_time must be before end_time")

        if not self.user_repo.exists(user_id):
            raise ValueError("User not found")
        if not self.pod_repo.exists(pod_id):
            raise ValueError("Pod not found")

        # kiểm tra trùng khung giờ
        if self.booking_repo.has_conflict(pod_id, start_time, end_time):
            raise ValueError("Time slot conflicts")

        # mặc định tạo ở PENDING
        return self.booking_repo.create(
            user_id=user_id,
            pod_id=pod_id,
            start_time=start_time,
            end_time=end_time,
            status="PENDING",
        )

    def get_customer_profile(self, user_id: int) -> dict:
        return self.user_repo.get_profile(user_id)

    def list_customer_bookings(
        self,
        user_id: int,
        status: Optional[str],
        dt_from: Optional[str],
        dt_to: Optional[str],
        page: int,
        limit: int,
    ):
        return self.booking_repo.list_for_customer(
            user_id=user_id,
            status=status,
            dt_from=dt_from,
            dt_to=dt_to,
            page=page,
            limit=limit,
        )

    # ---------- STAFF ----------
    def list_staff_bookings(
        self,
        status: Optional[str],
        user_id: Optional[int],
        pod_id: Optional[int],
        dt_from: Optional[str],
        dt_to: Optional[str],
        page: int,
        limit: int,
    ):
        return self.booking_repo.list_for_staff(
            status=status,
            user_id=user_id,
            pod_id=pod_id,
            dt_from=dt_from,
            dt_to=dt_to,
            page=page,
            limit=limit,
        )

    def check_in(self, booking_id: int, at_time: Optional[datetime] = None):
        bk = self.booking_repo.get_by_id(booking_id)
        if not bk:
            raise ValueError("Booking not found")

        # Cho phép từ PENDING hoặc CONFIRMED
        if bk.status not in ("PENDING", "CONFIRMED"):
            raise ValueError("Booking not in valid state for check-in")

        now = at_time or datetime.utcnow()
        if bk.start_time and now < bk.start_time:
            raise ValueError("Check-in only allowed at/after start_time")

        bk.status = "CHECKED_IN"
        bk.updated_at = now
        return self.booking_repo.update(bk)

    def check_out(self, booking_id: int, at_time: Optional[datetime] = None):
        bk = self.booking_repo.get_by_id(booking_id)
        if not bk:
            raise ValueError("Booking not found")

        if bk.status != "CHECKED_IN":
            raise ValueError("Booking not in valid state for check-out")

        now = at_time or datetime.utcnow()
        bk.status = "CHECKED_OUT"
        bk.updated_at = now

        # (tùy chọn) tính tiền nếu có đủ dữ liệu
        try:
            if bk.start_time and bk.end_time and bk.pod and bk.pod.price is not None:
                duration_hours = (bk.end_time - bk.start_time).total_seconds() / 3600.0
                bk.total_price = float(duration_hours) * float(bk.pod.price)
        except Exception:
            # tránh làm hỏng flow nếu quan hệ chưa eagerload
            pass

        return self.booking_repo.update(bk)
