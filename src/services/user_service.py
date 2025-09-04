from sqlalchemy.orm import Session
from ..infrastructure.repositories.user_repository import UserRepository
from ..api.requests import verify_password, hash_password
from ..domain.exceptions import AppError

class UserService:
    def __init__(self, session: Session):
        self.users = UserRepository(session)
        self.db = session

    def get_me(self, user_id: int):
        u = self.users.get_by_id(user_id)
        return {"id": u.id, "email": u.email, "full_name": u.full_name, "role": u.role.name}

    def update_me(self, user_id: int, full_name: str | None = None):
        u = self.users.get_by_id(user_id)
        if full_name:
            u.full_name = full_name
        self.db.commit()
        return {"id": u.id, "email": u.email, "full_name": u.full_name, "role": u.role.name}

    def change_email(self, user_id: int, new_email: str):
        if self.users.get_by_email(new_email):
            raise AppError("Email already in use", 400)
        u = self.users.get_by_id(user_id)
        u.email = new_email
        self.db.commit()
        return {"id": u.id, "email": u.email, "full_name": u.full_name, "role": u.role.name}

    def change_password(self, user_id: int, old_pw: str, new_pw: str):
        u = self.users.get_by_id(user_id)
        if not verify_password(old_pw, u.password):
            raise AppError("Wrong password", 400)
        u.password = hash_password(new_pw)
        self.db.commit()
