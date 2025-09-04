from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from .base import Base, TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "Users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("Roles.id"), nullable=False)

    role = relationship("Role", back_populates="users")
    bookings = relationship("Booking", back_populates="user")
