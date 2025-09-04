from sqlalchemy.orm import Session
from ..models.user import User
from ..models.role import Role

class UserRepository:
    def __init__(self, session: Session):
        self.db = session

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_role_by_name(self, role_name: str):
        return self.db.query(Role).filter(Role.name == role_name).first()

    def add(self, user: User):
        self.db.add(user)
        self.db.flush()
        return user

    def list_all(self):
        return self.db.query(User).all()

    def delete(self, user: User):
        self.db.delete(user)
