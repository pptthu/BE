# domain/models/ilocation_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from .location import Location


class ILocationRepository(ABC):
    @abstractmethod
    def add(self, location: Location) -> Location:
        """Thêm Location mới, trả về Location đã được gán id."""
        pass

    @abstractmethod
    def get_by_id(self, location_id: int) -> Optional[Location]:
        """Lấy Location theo id, không có thì trả None."""
        pass

    @abstractmethod
    def list(self) -> List[Location]:
        """Trả về danh sách tất cả Location."""
        pass

    @abstractmethod
    def update(self, location: Location) -> Location:
        """Cập nhật Location, trả về bản ghi sau cập nhật."""
        pass

    @abstractmethod
    def delete(self, location_id: int) -> None:
        """Xoá Location theo id."""
        pass
