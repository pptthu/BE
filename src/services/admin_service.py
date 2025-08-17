from src.infrastructure.models.user_model import UserModel
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
        return user

    @staticmethod
    def delete_user(user_id: int):
        """Xóa user."""
        user = session.query(UserModel).filter_by(id=user_id).first()
        if not user:
            return None
        session.delete(user)
        session.commit()
        return user
