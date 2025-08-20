from src.infrastructure.models.service_model import Service
from src.infrastructure.repositories.base import BaseRepository
class ServiceRepository(BaseRepository[Service]):
    def __init__(self): super().__init__(Service)
