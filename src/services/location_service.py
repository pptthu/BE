from infrastructure.models.location_model import LocationModel
from infrastructure.databases.mssql import session
from datetime import datetime

class LocationService:
    def list_locations(self):
        return session.query(LocationModel).all()

    def get_location(self, location_id):
        return session.query(LocationModel).get(location_id)

    def create_location(self, data):
        location = LocationModel(
            name=data["name"],
            address=data.get("address"),
            description=data.get("description"),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(location)
        session.commit()
        return location

    def update_location(self, location_id, data):
        location = session.query(LocationModel).get(location_id)
        if not location:
            return None
        location.name = data.get("name", location.name)
        location.address = data.get("address", location.address)
        location.description = data.get("description", location.description)
        location.updated_at = datetime.utcnow()
        session.commit()
        return location

    def delete_location(self, location_id):
        location = session.query(LocationModel).get(location_id)
        if location:
            session.delete(location)
            session.commit()
