from src.infrastructure.models.user_model import User
from src.infrastructure.repositories.base import BaseRepository
from src.infrastructure.databases.extensions import db
from typing import Optional
class UserRepository(BaseRepository[User]):
    def __init__(self): super().__init__(User)
    def by_email(self, email:str)->Optional[User]: return User.query.filter_by(email=email).first()
    def soft_disable(self, _id:int)->bool:
        u = self.get(_id)
        if not u: return False
        u.is_active = False; db.session.commit(); return True
