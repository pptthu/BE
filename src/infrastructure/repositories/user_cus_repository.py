# src/infrastructure/repositories/user_cus_repository.py
from __future__ import annotations
from typing import List, Optional
from datetime import datetime
from domain.models.iuser_repository import IUserRepository
from domain.models.user_cus import User

class UserRepository(IUserRepository):
    def __init__(self):
        self._users: List[User] = []
        self._id_counter: int = 1

    # CRUD cơ bản (in-memory demo)
    def add(self, user: User) -> User:
        user.id = self._id_counter
        self._id_counter += 1
        self._users.append(user)
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        for u in self._users:
            if u.id == user_id:
                return u
        return None

    def list(self) -> List[User]:
        return self._users

    def update(self, user: User) -> User:
        for idx, u in enumerate(self._users):
            if u.id == user.id:
                self._users[idx] = user
                return user
        raise ValueError("User not found")

    def delete(self, user_id: int) -> None:
        self._users = [u for u in self._users if u.id != user_id]

    # Bổ sung cho service
    def get_by_username(self, username: str) -> Optional[User]:
        for u in self._users:
            if u.username == username:
                return u
        return None

    # Helpers cho Customer API
    def exists(self, user_id: int) -> bool:
        return any(u.id == user_id for u in self._users)

    def get_profile(self, user_id: int) -> dict:
        u = self.get_by_id(user_id)
        if not u:
            return {}
        return {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "roles_id": u.roles_id,
            "preferred_location_id": u.preferred_location_id,
            "created_at": u.created_at,
            "updated_at": u.updated_at,
        }
