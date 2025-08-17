from typing import Optional, List
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from src.infrastructure.models.user_model import UserModel
from src.infrastructure.models.role_model import RoleModel

class UserService:
    @staticmethod
    def get_by_email(session, email: str) -> Optional[UserModel]:
        return (
            session.query(UserModel)
            .filter(func.lower(UserModel.email) == email.lower())
            .first()
        )

    @staticmethod
    def verify_password(user: UserModel, plaintext: str) -> bool:
        return check_password_hash(user.password, plaintext)

    @staticmethod
    def create_user(session, full_name: str, email: str, password: str, role_name: str = "customer") -> UserModel:
        if UserService.get_by_email(session, email):
            raise ValueError("Email already in use.")
        role = session.query(RoleModel).filter(RoleModel.name == role_name).first()
        if not role:
            raise LookupError("Role not found.")
        hashed = generate_password_hash(password)
        user = UserModel(full_name=full_name, email=email, password=hashed, role_id=role.id)
        session.add(user); session.commit(); session.refresh(user)
        return user

    @staticmethod
    def list_all(session) -> List[UserModel]:
        return session.query(UserModel).order_by(UserModel.id.asc()).all()

    @staticmethod
    def assign_role(session, user_id: int, role_name: str) -> UserModel:
        user = session.get(UserModel, user_id)
        if not user:
            raise LookupError("User not found")
        role = session.query(RoleModel).filter_by(name=role_name).first()
        if not role:
            raise LookupError("Role not found")
        user.role_id = role.id
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def delete_user(session, user_id: int):
        user = session.get(UserModel, user_id)
        if not user:
            raise LookupError("User not found")
        session.delete(user)
        session.commit()

