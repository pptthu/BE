from typing import List, Optional
from domain.models.ipod_repository import IPodRepository
from domain.models.pod import Pod

class PodRepository(IPodRepository):
    """
    Repository lưu tạm trong RAM (in-memory demo).
    Khi kết nối DB thì thay bằng phiên bản ORM.
    """
    def __init__(self):
        self._pods: List[Pod] = []
        self._id_counter: int = 1

    def add(self, pod: Pod) -> Pod:
        pod.id = self._id_counter
        self._id_counter += 1
        self._pods.append(pod)
        return pod

    def get_by_id(self, pod_id: int) -> Optional[Pod]:
        for p in self._pods:
            if p.id == pod_id:
                return p
        return None

    def list(self) -> List[Pod]:
        return self._pods

    def update(self, pod: Pod) -> Pod:
        for idx, p in enumerate(self._pods):
            if p.id == pod.id:
                self._pods[idx] = pod
                return pod
        raise ValueError("Pod not found")

    def delete(self, pod_id: int) -> None:
        self._pods = [p for p in self._pods if p.id != pod_id]
