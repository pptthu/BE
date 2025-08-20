﻿from src.infrastructure.models.location_model import Location
from src.infrastructure.repositories.base import BaseRepository
class LocationRepository(BaseRepository[Location]):
    def __init__(self): super().__init__(Location)
