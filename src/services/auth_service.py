# src/services/auth_service.py
from typing import Optional, Dict, Any
from domain.models.iuser_repository import IUserRepository
from domain.models.user import User


class AuthService:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    # Đăng ký tài khoản (tạo user mới)
    def register(
        self,
        username: str,
        email: str,
        password: str,
        roles_id: int,
        created_at,
        updated_at,
    ) -> User:
        # chuẩn hoá tối thiểu đầu vào
        username = (username or "").strip()
        email = (email or "").strip()
        if not username or not email or not password:
            # theo khung: không raise custom; service để controller/schema validate
            # nhưng thêm check này để tránh tạo user rỗng khi gọi sai.
            raise ValueError("username, email, password là bắt buộc")

        user = User(
            id=None,
            username=username,
            email=email,
            password=password,     # nếu dùng hash thì repo chịu trách nhiệm lưu hash
            roles_id=roles_id,
            created_at=created_at,
            updated_at=updated_at,
        )
        return self.repository.add(user)

    # Đăng nhập (xác thực tối giản)
    def login(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        username = (username or "").strip()
        if not username or not password:
            return None

        user = self.repository.get_by_username(username)
        if not user:
            return None

        # Tối giản: so sánh plain text; nếu repo lưu hash, repo nên đảm nhiệm việc so khớp
        if getattr(user, "password", None) != password:
            return None

        return {
            "user_id": getattr(user, "id", None),
            "username": getattr(user, "username", None),
            "email": getattr(user, "email", None),
            "roles_id": getattr(user, "roles_id", None),
        }

    # Đổi mật khẩu (tối giản)
    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        if not user_id or not old_password or not new_password:
            return False

        user = self.repository.get_by_id(user_id)
        if not user:
            return False

        if getattr(user, "password", None) != old_password:
            return False

        user.password = new_password
        self.repository.update(user)
        return True

    # Tiện ích: lấy user theo id
    def get_user(self, user_id: int) -> Optional[User]:
        if not user_id:
            return None
        return self.repository.get_by_id(user_id)
