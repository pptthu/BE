# src/infrastructure/repositories/booking_repository.py
from __future__ import annotations
from typing import List, Optional, Tuple
from datetime import datetime

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from infrastructure.databases.mssql import session
from infrastructure.models.booking_model import BookingModel
from infrastructure.models.users_model import UserModel  # ensure only ONE UserModel exists

def _parse_iso(s: Optional[str]) -> Optional[datetime]:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None

class BookingRepository:
    def __init__(self):
        self.session: Session = session

    # ---- dùng cho Customer ----
    def has_conflict(self, pod_id, start_time, end_time) -> bool:
        # overlap: NOT (end <= start_new OR start >= end_new)
        q = (
            self.session.query(BookingModel.id)
            .filter(BookingModel.pod_id == pod_id)
            .filter(
                ~(
                    (BookingModel.end_time <= start_time)
                    | (BookingModel.start_time >= end_time)
                )
            )
        )
        return self.session.query(q.exists()).scalar()

    def create(self, user_id, pod_id, start_time, end_time, status):
        bk = BookingModel(
            user_id=user_id,
            pod_id=pod_id,
            start_time=start_time,
            end_time=end_time,
            status=status,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.session.add(bk)
        self.session.commit()
        self.session.refresh(bk)
        return bk

    def list_for_customer(
        self,
        user_id: int,
        status: Optional[str],
        dt_from: Optional[str],
        dt_to: Optional[str],
        page: int,
        limit: int,
    ) -> Tuple[List[BookingModel], int]:
        q = self.session.query(BookingModel).filter(BookingModel.user_id == user_id)

        if status:
            q = q.filter(func.upper(BookingModel.status) == status.upper())

        dt_from_dt = _parse_iso(dt_from)
        if dt_from_dt:
            q = q.filter(BookingModel.end_time >= dt_from_dt)
        dt_to_dt = _parse_iso(dt_to)
        if dt_to_dt:
            q = q.filter(BookingModel.start_time <= dt_to_dt)

        total = q.order_by(None).count()
        items = (
            q.order_by(BookingModel.start_time.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )
        return items, total

    # ---- dùng cho Staff ----
    def list_for_staff(
        self,
        status: Optional[str],
        user_id: Optional[int],
        pod_id: Optional[int],
        dt_from: Optional[str],
        dt_to: Optional[str],
        page: int,
        limit: int,
    ) -> Tuple[List[BookingModel], int]:
        q = self.session.query(BookingModel).options(joinedload(BookingModel.user))

        if status:
            q = q.filter(func.upper(BookingModel.status) == status.upper())
        if user_id:
            q = q.filter(BookingModel.user_id == user_id)
        if pod_id:
            q = q.filter(BookingModel.pod_id == pod_id)

        dt_from_dt = _parse_iso(dt_from)
        if dt_from_dt:
            q = q.filter(BookingModel.end_time >= dt_from_dt)
        dt_to_dt = _parse_iso(dt_to)
        if dt_to_dt:
            q = q.filter(BookingModel.start_time <= dt_to_dt)

        total = q.order_by(None).count()
        items = (
            q.order_by(BookingModel.start_time.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )
        return items, total

    # Common
    def get_by_id(self, booking_id: int) -> Optional[BookingModel]:
        return self.session.get(BookingModel, booking_id)

    def update(self, booking: BookingModel) -> BookingModel:
        self.session.add(booking)
        self.session.commit()
        self.session.refresh(booking)
        return booking
