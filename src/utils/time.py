from datetime import datetime, timedelta

def now():
    return datetime.utcnow()

def to_iso(dt: datetime):
    return dt.isoformat() + "Z" if dt else None

def add_hours(dt: datetime, hours: int):
    return dt + timedelta(hours=hours)
