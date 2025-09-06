from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from .base import Base, TimestampMixin

class Role(Base, TimestampMixin):
    __tablename__ = "Roles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    users = relationship("User", back_populates="role")
