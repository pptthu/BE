from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from src.infrastructure.databases.mssql import Base

class UserModel(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("Roles.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.getdate())
    updated_at = Column(DateTime, nullable=False, server_default=func.getdate())

    role = relationship("RoleModel", back_populates="users")
    bookings = relationship("BookingModel", back_populates="user")
