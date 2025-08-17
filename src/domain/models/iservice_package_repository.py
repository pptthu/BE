from abc import ABC, abstractmethod
from typing import List, Optional
from .service_package import ServicePackage


class IServicePackageRepository(ABC):
    @abstractmethod
    def add(self, pkg: ServicePackage) -> ServicePackage:
        """Thêm gói dịch vụ mới, trả về bản ghi đã gán id."""
        pass

    @abstractmethod
    def get_by_id(self, package_id: int) -> Optional[ServicePackage]:
        """Lấy gói dịch vụ theo id; không có thì None."""
        pass

    @abstractmethod
    def list(self) -> List[ServicePackage]:
        """Trả về danh sách tất cả gói dịch vụ."""
        pass

    @abstractmethod
    def update(self, pkg: ServicePackage) -> ServicePackage:
        """Cập nhật gói dịch vụ, trả về bản ghi sau cập nhật."""
        pass

    @abstractmethod
    def delete(self, package_id: int) -> bool:
        """Xoá gói dịch vụ theo id; trả True nếu xoá được."""
        pass
