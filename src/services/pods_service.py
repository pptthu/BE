import datetime as dt
from sqlalchemy.orm import Session
from ..infrastructure.repositories.pod_repository import PODRepository
from ..infrastructure.models.pod import POD
from ..infrastructure.models.booking import Booking

def _parse_iso(x: str | None):
    if not x:
        return None
    try:
        return dt.datetime.fromisoformat(x.replace("Z", ""))
    except Exception:
        return None

class PodsService:
    def __init__(self, session: Session):
        self.db = session
        self.pods = PODRepository(session)

    def list_pods(self, location_id: int | None, start_time: str | None = None, end_time: str | None = None):
        items_query = self.db.query(POD)
        if location_id:
            items_query = items_query.filter(POD.location_id == location_id)

        start = _parse_iso(start_time)
        end = _parse_iso(end_time)

        if start and end and end > start:
            # loại bỏ POD có booking chồng lấn: existing.start < end AND existing.end > start
            overlap = self.db.query(Booking.id).filter(
                Booking.pod_id == POD.id,
                Booking.status.in_(["PENDING", "CONFIRMED", "CHECKED_IN"]),
                Booking.start_time < end,
                Booking.end_time > start
            ).exists()
            items_query = items_query.filter(~overlap)

        items = items_query.all()
        return [
            {"id": p.id, "name": p.name, "price": float(p.price), "status": p.status, "location_id": p.location_id}
            for p in items
        ]

    def get_pod(self, pod_id: int):
        p = self.pods.get(pod_id)
        if not p:
            return None
        return {"id": p.id, "name": p.name, "price": float(p.price), "status": p.status, "location_id": p.location_id}
