from typing import List, Optional
from sqlalchemy import func
from src.infrastructure.models.location_model import LocationModel

class LocationService:
    @staticmethod
    def create(session, name: str, address: str) -> LocationModel:
        exists = (session.query(LocationModel)
                  .filter(func.lower(LocationModel.name) == name.lower())
                  .first())
        if exists: raise ValueError("Location name already exists.")
        loc = LocationModel(name=name, address=address)
        session.add(loc); session.commit(); session.refresh(loc); return loc

    @staticmethod
    def list_all(session) -> List[LocationModel]:
        return session.query(LocationModel).order_by(LocationModel.id.asc()).all()

    @staticmethod
    def get_by_name(session, name: str) -> Optional[LocationModel]:
        return (session.query(LocationModel)
                .filter(func.lower(LocationModel.name) == name.lower())
                .first())
