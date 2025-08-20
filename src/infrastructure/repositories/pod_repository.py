from src.infrastructure.models.pod_model import POD
from src.infrastructure.repositories.base import BaseRepository
from typing import List
class PODRepository(BaseRepository[POD]):
    def __init__(self): super().__init__(POD)
    def list_by_location(self, location_id:int)->List[POD]:
        return POD.query.filter_by(location_id=location_id).all()
