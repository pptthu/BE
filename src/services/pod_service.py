from typing import List, Optional
from domain.models.pod import Pod
from domain.models.ipod_repository import IPodRepository


class PodService:
    def __init__(self, repository: IPodRepository):
        self.repository = repository

    def create_pod(self, name: str, location_id: int, price: float, status: str, created_at, updated_at) -> Pod:
        if not name or not location_id:
            raise ValueError("name và location_id là bắt buộc")

        pod = Pod(
            id=None,
            name=name.strip(),
            location_id=location_id,
            price=price,
            status=status,
            created_at=created_at,
            updated_at=updated_at
        )
        return self.repository.add(pod)

    def get_pod(self, pod_id: int) -> Optional[Pod]:
        return self.repository.get_by_id(pod_id)

    def list_pods(self) -> List[Pod]:
        return self.repository.list()

    def update_pod(self, pod_id: int, name: str, location_id: int, price: float, status: str, created_at, updated_at) -> Pod:
        if not pod_id:
            raise ValueError("pod_id là bắt buộc")

        pod = Pod(
            id=pod_id,
            name=name.strip(),
            location_id=location_id,
            price=price,
            status=status,
            created_at=created_at,
            updated_at=updated_at
        )
        return self.repository.update(pod)

    def delete_pod(self, pod_id: int) -> None:
        self.repository.delete(pod_id)
