# src/infrastructure/repositories/booking_repository.py
from __future__ import annotations

from typing import Optional, List, Dict, Any
from datetime import datetime, date, time

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models.booking import Booking
from ..models.pod import POD as PodEntity

_ACTIVE_BOOKING_STATUSES = ("PENDING", "CONFIRMED", "CHECKED_IN")


class BookingRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    # ------------------------------ Helpers ------------------------------ #
    def _overlap_filter(self, pod_id: int, st: datetime, et: datetime):
        return (
            Booking.pod_id == pod_id,
            Booking.status.in_(_ACTIVE_BOOKING_STATUSES),
            Booking.start_time < et,
            Booking.end_time > st,
        )

    # ------------------------------ Queries ------------------------------ #
    def has_overlap(
        self,
        pod_id: int,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        *,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> bool:
        st = start_time or start
        et = end_time or end
        if st is None or et is None:
            raise ValueError("start/end (hoặc start_time/end_time) là bắt buộc")

        cnt = (
            self.db.query(func.count(Booking.id))
            .filter(*self._overlap_filter(pod_id, st, et))
            .scalar()
        ) or 0
        return cnt > 0

    def get_by_id(self, booking_id: int) -> Optional[Booking]:
        try:
            return self.db.get(Booking, booking_id)  # SA 2.0
        except AttributeError:
            return self.db.query(Booking).get(booking_id)  # type: ignore  # SA 1.4

    def list_by_user(self, user_id: int) -> List[Booking]:
        return (
            self.db.query(Booking)
            .filter(Booking.user_id == user_id)
            .order_by(Booking.start_time.desc())
            .all()
        )

    def list_for_staff_today(self) -> List[Booking]:
        today = date.today()
        start_of_day = datetime.combine(today, time.min)
        end_of_day = datetime.combine(today, time.max)
        return (
            self.db.query(Booking)
            .filter(
                Booking.start_time <= end_of_day,
                Booking.end_time >= start_of_day,
            )
            .order_by(Booking.start_time.asc())
            .all()
        )

    def get_pod(self, pod_id: int):
        try:
            return self.db.get(PodEntity, pod_id)
        except AttributeError:
            return self.db.query(PodEntity).get(pod_id)  # type: ignore

    # ----------------------------- Mutations ----------------------------- #
    def create(
        self,
        *,
        user_id: int,
        pod_id: int,
        start_time: datetime,
        end_time: datetime,
        status: str = "PENDING",
        total_price: Optional[float] = None,
    ) -> Booking:
        payload: Dict[str, Any] = {
            "user_id": user_id,
            "pod_id": pod_id,
            "start_time": start_time,
            "end_time": end_time,
            "status": status,
        }
        if total_price is not None and hasattr(Booking, "total_price"):
            payload["total_price"] = total_price

        booking = Booking(**payload)
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def add(self, *args, **kwargs) -> Booking:
        """
        Chấp nhận mọi kiểu gọi:
        - repo.add(user_obj, {...})
        - repo.add(user_obj, pod_id, start_time, end_time[, status[, total_price]])
        - repo.add(user_id, {...}) hoặc repo.add(user_id, pod_id, start_time, end_time, ...)
        - repo.add({...})
        - repo.add(user_id=..., pod_id=..., start_time=..., end_time=..., ...)
        Tự chuẩn hoá 'start|startTime' -> 'start_time', 'end|endTime' -> 'end_time'.
        """
        user_id = None
        data: Dict[str, Any] = {}

        def _get_id_like(v):
            if v is None:
                return None
            if hasattr(v, "id"):
                try:
                    return int(getattr(v, "id"))
                except Exception:
                    return None
            if isinstance(v, (int, str)):
                try:
                    return int(v)
                except Exception:
                    return None
            return None

        # (A) add(user_like, dict_payload)
        if len(args) >= 2 and isinstance(args[1], dict):
            user_id = _get_id_like(args[0])
            data = dict(args[1])

        # (B) add(user_like, pod_id, start_time, end_time[, status[, total_price]])
        elif len(args) >= 4 and _get_id_like(args[0]) is not None:
            user_id = _get_id_like(args[0])
            data = {
                "pod_id": args[1],
                "start_time": args[2],
                "end_time": args[3],
            }
            if len(args) >= 5 and args[4] is not None:
                data["status"] = args[4]
            if len(args) >= 6 and args[5] is not None:
                data["total_price"] = args[5]

        # (C) add(dict_payload)
        elif len(args) == 1 and isinstance(args[0], dict):
            data = dict(args[0])

        # (D) add(**kwargs)
        else:
            data = dict(kwargs)
            user_id = _get_id_like(
                kwargs.get("user")
                or kwargs.get("current_user")
                or kwargs.get("user_id")
            )

        # Ưu tiên user_id từ payload
        if "user_id" in data and data["user_id"] is not None:
            user_id = _get_id_like(data["user_id"])
        if user_id is not None:
            data["user_id"] = user_id

        # CamelCase -> snake_case & alias start/end
        if "pod_id" not in data and "podId" in data:
            data["pod_id"] = data.pop("podId")
        if "start_time" not in data and "startTime" in data:
            data["start_time"] = data.pop("startTime")
        if "end_time" not in data and "endTime" in data:
            data["end_time"] = data.pop("endTime")
        if "start_time" not in data and "start" in data:
            data["start_time"] = data.pop("start")
        if "end_time" not in data and "end" in data:
            data["end_time"] = data.pop("end")

        allowed = {"user_id", "pod_id", "start_time", "end_time", "status", "total_price"}
        data = {k: v for k, v in data.items() if k in allowed and v is not None}

        missing = [k for k in ("user_id", "pod_id", "start_time", "end_time") if k not in data]
        if missing:
            raise ValueError(f"Missing fields: {', '.join(missing)}")

        return self.create(**data)

    def update_status(self, booking_id: int, status: str) -> Optional[Booking]:
        booking = self.get_by_id(booking_id)
        if not booking:
            return None
        booking.status = status
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def confirm_payment(self, booking_id: int) -> Optional[Booking]:
        return self.update_status(booking_id, "CONFIRMED")

    def checkin(self, booking_id: int) -> Optional[Booking]:
        return self.update_status(booking_id, "CHECKED_IN")

    def checkout(self, booking_id: int) -> Optional[Booking]:
        return self.update_status(booking_id, "COMPLETED")
