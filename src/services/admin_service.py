from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from infrastructure.models.user_model import User


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
        return user

    @staticmethod
    def delete_user(user_id: int):
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
        return user
