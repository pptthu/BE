from sqlalchemy.orm import Session
from ..infrastructure.repositories.user_repository import UserRepository
from ..infrastructure.models.user import User
from ..infrastructure.models.role import Role
from ..infrastructure.models.base import now_utc
from ..domain.exceptions import AppError
from ..config import load_config
from ..api.requests import hash_password, verify_password, create_jwt

_CFG = load_config()

class AuthService:
    def __init__(self, session: Session):
        self.db = session
        self.users = UserRepository(session)

    def _ensure_role(self, role_name: str):
        role = self.users.get_role_by_name(role_name)
        if not role:
            role = Role(name=role_name, created_at=now_utc(), updated_at=now_utc())
            self.db.add(role)
            self.db.flush()
        return role

    def _users_count(self) -> int:
        return self.db.query(User).count()

    def register_customer(self, full_name: str, email: str, password: str):
        if self.users.get_by_email(email):
            raise AppError("Email already registered", 400)

        first_user_admin = bool(_CFG.get("FIRST_USER_ADMIN", True))
        role_name = "ADMIN" if (first_user_admin and self._users_count() == 0) else "CUSTOMER"
        role = self._ensure_role(role_name)

        u = User(
            full_name=full_name,
            email=email,
            password=hash_password(password),
            role_id=role.id,
            created_at=now_utc(),
            updated_at=now_utc()
        )
        self.users.add(u)
        self.db.commit()
        return u

    def login(self, email: str, password: str):
        u = self.users.get_by_email(email)
        if not u or not verify_password(password, u.password):
            return None, None
        token = create_jwt({"id": u.id, "email": u.email, "role": u.role.name})
        return token, u
