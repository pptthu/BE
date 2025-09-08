from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Numeric
from decimal import Decimal
from .base import Base, TimestampMixin

class POD(Base, TimestampMixin):
    __tablename__ = "PODs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="AVAILABLE")
    location_id: Mapped[int] = mapped_column(ForeignKey("Locations.id"), nullable=False)

    location = relationship("Location", back_populates="pods")
    bookings = relationship("Booking", back_populates="pod")
