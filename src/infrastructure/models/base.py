from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import DateTime
import datetime as dt

Base = declarative_base()

def now_utc():
    return dt.datetime.utcnow()

class TimestampMixin:
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=now_utc, nullable=False)
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime, default=now_utc, onupdate=now_utc, nullable=False)
