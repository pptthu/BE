# src/infrastructure/repositories/user_repository.py
from domain.models.iuser_repository import IUserRepository
from domain.models.user import User
from typing import List, Optional
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Config
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from infrastructure.databases import Base

load_dotenv()


class UserRepository(IUserRepository):
    def __init__(self):
        # Bộ nhớ giả lập (in-memory) để chứa users
        self._users: List[User] = []
        self._id_counter: int = 1   # tự tăng ID giống database

    # ---------------- CRUD cơ bản ----------------
    def add(self, user: User) -> User:
        """
        Thêm user mới vào danh sách (giả lập insert DB).
        - Tự gán ID tăng dần.
        - Trả về user sau khi thêm.
        """
        user.id = self._id_counter
        self._id_counter += 1
        self._users.append(user)
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Tìm user theo ID.
        - Nếu có thì trả về User.
        - Nếu không có thì trả về None.
        """
        for u in self._users:
            if u.id == user_id:
                return u
        return None

    def list(self) -> List[User]:
        """
        Lấy toàn bộ danh sách user.
        (tương tự SELECT * FROM users).
        """
        return self._users

    def update(self, user: User) -> User:
        """
        Cập nhật thông tin user.
        - Tìm user trong list theo ID.
        - Nếu thấy thì thay thế bằng user mới.
        - Nếu không thấy thì raise error.
        """
        for idx, u in enumerate(self._users):
            if u.id == user.id:
                self._users[idx] = user
                return user
        raise ValueError('User not found')

    def delete(self, user_id: int) -> None:
        """
        Xoá user theo ID.
        - Nếu có thì xoá khỏi list.
        - Nếu không có thì không làm gì.
        """
        self._users = [u for u in self._users if u.id != user_id]

    # ---------------- Bổ sung cho Auth ----------------
    def get_by_username(self, username: str) -> Optional[User]:
        """
        Tìm user theo username.
        - Dùng khi login để check tài khoản.
        """
        for u in self._users:
            if u.username == username:
                return u
        return None

    def add_user(self, username: str, email: str, password: str, roles_id: int, created_at, updated_at) -> User:
        """
        Đăng ký user mới.
        - Nhận các field cơ bản của user.
        - Trả về user đã được thêm.
        """
        user = User(
            id=None,
            username=username,
            email=email,
            password=password,   # nếu dùng hash thì truyền password hash vào
            roles_id=roles_id,
            created_at=created_at,
            updated_at=updated_at
        )
        return self.add(user)

    def update_user(self, user: User) -> User:
        """
        Cập nhật user.
        - Có thể dùng khi đổi mật khẩu, đổi email, đổi role...
        """
        return self.update(user)


# ---------------- ORM Model ----------------
# Dùng SQLAlchemy để ánh xạ với bảng users trong database thực.
class UserModel(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)   # nếu lưu hash, nên đổi thành password_hash
    roles_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
