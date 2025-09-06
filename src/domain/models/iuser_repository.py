# domain/models/iuser_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from .user_cus import User


class IUserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> User:
        """Thêm một user mới, trả về user đã được gán id."""
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Lấy user theo id, không có thì trả None."""
        pass

    @abstractmethod
    def list(self) -> List[User]:
        """Trả về toàn bộ user."""
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """Cập nhật user, trả về user sau cập nhật."""
        pass

   

    # Thêm cho auth_service
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """Lấy user theo username."""
        pass
