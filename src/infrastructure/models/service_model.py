from sqlalchemy import Column, Integer, String, Numeric
from src.infrastructure.databases.mssql import Base

class ServiceModel(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
