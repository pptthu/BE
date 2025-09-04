from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from .base import Base, TimestampMixin

class Location(Base, TimestampMixin):
    __tablename__ = "Locations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)

    pods = relationship("POD", back_populates="location")
