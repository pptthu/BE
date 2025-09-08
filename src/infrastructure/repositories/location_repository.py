from sqlalchemy.orm import Session
from ..models.location import Location

class LocationRepository:
    def __init__(self, session: Session):
        self.db = session

    def list(self):
        return self.db.query(Location).all()

    def get(self, loc_id: int):
        return self.db.query(Location).filter(Location.id == loc_id).first()

    def add(self, loc: Location):
        self.db.add(loc)
        self.db.flush()
        return loc

    def delete(self, loc: Location):
        self.db.delete(loc)
