from typing import List, Optional
from domain.models.iservice_package_repository import IServicePackageRepository
from domain.models.service_package import ServicePackage


class ServicePackageRepository(IServicePackageRepository):
    """
    Repository in-memory (giả lập). Khi gắn DB thật, tạo repo mới dùng Session.
    """
    def __init__(self):
        self._items: List[ServicePackage] = []
        self._id_counter: int = 1

    def add(self, pkg: ServicePackage) -> ServicePackage:
        pkg.id = self._id_counter
        self._id_counter += 1
        self._items.append(pkg)
        return pkg

    def get_by_id(self, package_id: int) -> Optional[ServicePackage]:
        for it in self._items:
            if it.id == package_id:
                return it
        return None

    def list(self) -> List[ServicePackage]:
        return self._items

    def update(self, pkg: ServicePackage) -> ServicePackage:
        for idx, it in enumerate(self._items):
            if it.id == pkg.id:
                self._items[idx] = pkg
                return pkg
        raise ValueError("Service package not found")

    def delete(self, package_id: int) -> bool:
        before = len(self._items)
        self._items = [it for it in self._items if it.id != package_id]
        return len(self._items) < before
