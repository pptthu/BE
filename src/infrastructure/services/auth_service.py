# src/infrastructure/services/auth_service.py
from datetime import timedelta
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.user_model import User
from src.infrastructure.repositories.user_repository import UserRepository

class AuthService:
    def __init__(self, repo: UserRepository): self.repo = repo

    def register(self, db, email: str, password: str, full_name: str|None=None):
        if self.repo.get_by_email(email): raise ValueError("Email đã tồn tại")
        user = User(email=email, password_hash=generate_password_hash(password), full_name=full_name)
        return self.repo.create(user)

    def login(self, email: str, password: str):
        user = self.repo.get_by_email(email)
        if not user or not check_password_hash(user.password_hash, password):
            raise ValueError("Sai email hoặc mật khẩu")
        token = create_access_token(identity={"id": user.id, "role": user.role}, expires_delta=timedelta(minutes=1440))
        return token, user
