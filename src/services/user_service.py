# src/services/user_service.py
from typing import List, Optional
from domain.models.user import User
from domain.models.iuser_repository import IUserRepository

class UserService:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        roles_id: int,
        created_at,
        updated_at,
    ) -> User:
        username = (username or "").strip()
        email = (email or "").strip()
        if not username or not email or not password:
            raise ValueError("username, email, password là bắt buộc")

        user = User(
            id=None,
            username=username,
            email=email,
            password=password,
            roles_id=roles_id,
            created_at=created_at,
            updated_at=updated_at,
        )
        return self.repository.add(user)

    def get_user(self, user_id: int) -> Optional[User]:
        if not user_id:
            return None
        return self.repository.get_by_id(user_id)

    def list_users(self) -> List[User]:
        return self.repository.list()

    def update_user(
        self,
        user_id: int,
        username: str,
        email: str,
        password: str,
        roles_id: int,
        created_at,
        updated_at,
    ) -> User:
        if not user_id:
            raise ValueError("user_id là bắt buộc")

        username = (username or "").strip()
        email = (email or "").strip()
        # CHÚ Ý: controller nên truyền password hiện tại nếu không muốn đổi password
        if not username or not email or password is None:
            raise ValueError("username, email, password không được rỗng")

        user = User(
            id=user_id,
            username=username,
            email=email,
            password=password,
            roles_id=roles_id,
            created_at=created_at,
            updated_at=updated_at,
        )
        return self.repository.update(user)

    def delete_user(self, user_id: int) -> None:
        if not user_id:
            raise ValueError("user_id là bắt buộc")
        self.repository.delete(user_id)
