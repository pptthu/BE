from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from src.infrastructure.databases.mssql import Base

class TodoModel(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
