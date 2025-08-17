from typing import List, Optional
from domain.models.service_package import ServicePackage
from domain.models.iservice_package_repository import IServicePackageRepository


class ServicePackageService:
    def __init__(self, repository: IServicePackageRepository):
        self.repository = repository

    def create_package(
        self,
        name: str,
        description: str | None,
        price: float,
        created_at,
        updated_at,
    ) -> ServicePackage:
        if not name or price is None:
            raise ValueError("name và price là bắt buộc")

        pkg = ServicePackage(
            id=None,
            name=name.strip(),
            description=(description or "").strip() if description else None,
            price=float(price),
            created_at=created_at,
            updated_at=updated_at,
        )
        return self.repository.add(pkg)

    def get_package(self, package_id: int) -> Optional[ServicePackage]:
        return self.repository.get_by_id(package_id)

    def list_packages(self) -> List[ServicePackage]:
        return self.repository.list()

    def update_package(
        self,
        package_id: int,
        name: str,
        description: str | None,
        price: float,
        created_at,
        updated_at,
    ) -> ServicePackage:
        if not package_id:
            raise ValueError("package_id là bắt buộc")

        pkg = ServicePackage(
            id=package_id,
            name=name.strip(),
            description=(description or "").strip() if description else None,
            price=float(price),
            created_at=created_at,
            updated_at=updated_at,
        )
        return self.repository.update(pkg)

    def delete_package(self, package_id: int) -> bool:
        return self.repository.delete(package_id)
