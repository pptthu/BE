from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from infrastructure.databases.base import Base
from sqlalchemy.orm import relationship

class UserModel(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    roles_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    bookings = relationship("BookingModel", back_populates="user")
    