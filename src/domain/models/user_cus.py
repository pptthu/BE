# domain/models/user.py
from datetime import datetime
from typing import Optional

class User:
    def __init__(
        self,
        id: Optional[int],
        username: str,
        email: str,
        password: str,        # lưu plain/hash tuỳ repo; service/repo sẽ chịu trách nhiệm
        roles_id: int,        # FK -> roles.id
        created_at: datetime,
        updated_at: datetime,
        preferred_location_id: Optional[int] = None,  
    ):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.roles_id = roles_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.preferred_location_id = preferred_location_id 

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username} roles_id={self.roles_id} preferred_location_id={self.preferred_location_id}>"
