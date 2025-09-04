from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Numeric, Boolean, DateTime
from decimal import Decimal
import datetime as dt
from .base import Base, TimestampMixin

class Booking(Base, TimestampMixin):
    __tablename__ = "Bookings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"), nullable=False)
    pod_id: Mapped[int] = mapped_column(ForeignKey("PODs.id"), nullable=False)

    start_time: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)
    end_time: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)

    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="PENDING")
    paid: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="bookings")
    pod = relationship("POD", back_populates="bookings")
