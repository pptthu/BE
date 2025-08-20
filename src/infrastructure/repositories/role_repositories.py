from src.infrastructure.models.role_model import Role
from src.infrastructure.repositories.base import BaseRepository

class RoleRepository(BaseRepository[Role]):
    def __init__(self):
        super().__init__(Role)
