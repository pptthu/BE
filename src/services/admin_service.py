<<<<<<< HEAD
from src.infrastructure.models.user import UserModel
from src.infrastructure.databases.mssql import session

class AdminService:
    """Service xử lý các nghiệp vụ của admin."""

    @staticmethod
    def get_all_users():
        """Lấy danh sách tất cả user."""
        return session.query(UserModel).all()

    @staticmethod
    def get_user_by_id(user_id: int):
        """Lấy thông tin user theo ID."""
        return session.query(UserModel).filter_by(id=user_id).first()

    @staticmethod
    def create_user(data: dict):
        """Tạo mới một user."""
        user = UserModel(**data)
        session.add(user)
        session.commit()
        return user

    @staticmethod
    def update_user(user_id: int, data: dict):
        """Cập nhật thông tin user."""
        user = session.query(UserModel).filter_by(id=user_id).first()
        if not user:
            return None
        for key, value in data.items():
            setattr(user, key, value)
        session.commit()
=======
<<<<<<< HEAD
from src.infrastructure.models.user import UserModel
from src.infrastructure.databases.mssql import session
=======
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from infrastructure.models.user_model import User

>>>>>>> origin/main

class AdminService:

    @staticmethod
    def login(email: str, password: str):
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            return user
        return None

 
    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def create_user(email: str, password: str, role: str = "Customer"):
        new_user = User(
            email=email,
            password=generate_password_hash(password),
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def update_user(user_id: int, data: dict):
        user = User.query.get(user_id)
        if not user:
            return None

        if "email" in data:
            user.email = data["email"]
        if "password" in data:
            user.password = generate_password_hash(data["password"])
        if "role" in data:
            user.role = data["role"]

        db.session.commit()
>>>>>>> origin/main
        return user

    @staticmethod
    def delete_user(user_id: int):
<<<<<<< HEAD
        """Xóa user."""
        user = session.query(UserModel).filter_by(id=user_id).first()
        if not user:
            return None
        session.delete(user)
        session.commit()
=======
        user = User.query.get(user_id)
        if not user:
            return False
        db.session.delete(user)
        db.session.commit()
        return True

 
    @staticmethod
    def assign_role(user_id: int, role: str):
        user = User.query.get(user_id)
        if not user:
            return None
        user.role = role
        db.session.commit()
>>>>>>> origin/main
        return user
