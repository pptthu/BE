from typing import List, Optional
from domain.models.location import Location
from domain.models.ilocation_repository import ILocationRepository

class LocationService:
    def __init__(self, repository: ILocationRepository):
        self.repository = repository

    def create_location(self, name: str, address: str, created_at, updated_at) -> Location:
        if not name or not address:
            raise ValueError("name và address là bắt buộc")

        location = Location(
            id=None,
            name=name.strip(),
            address=address.strip(),
            created_at=created_at,
            updated_at=updated_at
        )
        return self.repository.add(location)

    def get_location(self, location_id: int) -> Optional[Location]:
        return self.repository.get_by_id(location_id)

    def list_locations(self) -> List[Location]:
        return self.repository.list()

    def update_location(self, location_id: int, name: str, address: str, created_at, updated_at) -> Location:
        if not location_id:
            raise ValueError("location_id là bắt buộc")

        location = Location(
            id=location_id,
            name=name.strip(),
            address=address.strip(),
            created_at=created_at,
            updated_at=updated_at
        )
        return self.repository.update(location)

    def delete_location(self, location_id: int) -> None:
        self.repository.delete(location_id)
