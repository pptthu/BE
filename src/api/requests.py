from datetime import datetime

def parse_iso(value: str):
    return datetime.fromisoformat(value) if value else None
