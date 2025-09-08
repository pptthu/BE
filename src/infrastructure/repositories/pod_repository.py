from sqlalchemy.orm import Session
from ..models.pod import POD

class PODRepository:
    def __init__(self, session: Session):
        self.db = session

    def list(self, location_id: int | None = None):
        q = self.db.query(POD)
        if location_id:
            q = q.filter(POD.location_id == location_id)
        return q.all()

    def list_all(self):
        return self.db.query(POD).all()

    def get(self, pod_id: int):
        return self.db.query(POD).filter(POD.id == pod_id).first()

    def add(self, pod: POD):
        self.db.add(pod)
        self.db.flush()
        return pod

    def delete(self, pod: POD):
        self.db.delete(pod)
