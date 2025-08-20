# src/infrastructure/databases/mssql.py
import os
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from .base import Base

load_dotenv()

DB_USER = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Aa@123456")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "1433")
DB_NAME = os.getenv("DB_NAME", "BookSysDB")

# Driver ODBC 18, bật TrustServerCertificate cho local dev
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={DB_HOST},{DB_PORT};"
    f"DATABASE={DB_NAME};"
    f"UID={DB_USER};PWD={DB_PASSWORD};"
    "TrustServerCertificate=Yes;"
)

DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"

engine = create_engine(DATABASE_URI, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def init_db():
    # Import models để Base biết metadata
    from src.models.user_model import User
    from src.models.location_model import Location
    from src.models.pod_model import Pod
    from src.models.service_model import Service
    from src.models.booking_model import Booking
    from src.models.booking_service_model import BookingService
    Base.metadata.create_all(bind=engine)
