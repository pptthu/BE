# src/infrastructure/models/admin_model.py

from sqlalchemy import Column, Integer, String, DateTime, func
from src.infrastructure.databases.mssql import Base

class AdminModel(Base):
    """Model đại diện cho bảng admin."""
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)   # ⚡ hashed password (nên dùng bcrypt)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(String(20), default="admin")       # ví dụ: superadmin, manager
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Admin {self.user_name}>"
