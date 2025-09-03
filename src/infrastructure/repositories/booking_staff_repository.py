# src/infrastructure/repositories/booking_repository.py
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from infrastructure.databases.mssql import session
from infrastructure.models.booking_model import BookingModel
from infrastructure.models.users_model import UserModel

class BookingRepository:
    def __init__(self):
        self.session: Session = session

    def list_for_staff(self, date: Optional[str] = None) -> List[BookingModel]:
        """
        Lấy danh sách booking trong ngày (mặc định = ngày hôm nay).
        Có join sang User để lấy tên khách.
        """
        q = (
            self.session.query(BookingModel, UserModel.username.label("customer_name"))
            .join(UserModel, UserModel.id == BookingModel.user_id)
        )

        if date:
            q = q.filter(func.cast(BookingModel.start_time, func.DATE) == date)

        return q.all()

    def get_by_id(self, booking_id: int) -> Optional[BookingModel]:
        return self.session.get(BookingModel, booking_id)

    def update(self, booking: BookingModel) -> BookingModel:
        self.session.add(booking)
        self.session.commit()
        self.session.refresh(booking)
        return booking
