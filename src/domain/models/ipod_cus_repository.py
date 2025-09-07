from abc import ABC, abstractmethod
from typing import List, Optional
from .pod_cus import Pod


class IPodRepository(ABC):
    @abstractmethod
    def add(self, pod: Pod) -> Pod:
        """Thêm POD mới, trả về POD đã được gán id."""
        pass

    @abstractmethod
    def get_by_id(self, pod_id: int) -> Optional[Pod]:
        """Lấy POD theo id, không có thì trả None."""
        pass

    @abstractmethod
    def list(self) -> List[Pod]:
        """Trả về danh sách tất cả POD."""
        pass

    @abstractmethod
    def update(self, pod: Pod) -> Pod:
        """Cập nhật POD, trả về bản ghi sau cập nhật."""
        pass

    @abstractmethod
    def delete(self, pod_id: int) -> None:
        """Xoá POD theo id."""
        pass
