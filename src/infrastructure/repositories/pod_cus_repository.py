# src/infrastructure/repositories/pod_cus_repository.py
from __future__ import annotations
from typing import List, Optional
from domain.models.ipod_cus_repository import IPodRepository
from domain.models.pod_cus import Pod

class PodRepository(IPodRepository):
    def __init__(self):
        self._pods: List[Pod] = []
        self._id_counter: int = 1

    def add(self, pod: Pod) -> Pod:
        pod.id = self._id_counter
        self._id_counter += 1
        self._pods.append(pod)
        return pod

    def get_by_id(self, pod_id: int) -> Optional[Pod]:
        return next((p for p in self._pods if p.id == pod_id), None)

    def list(self) -> List[Pod]:
        return self._pods

    def update(self, pod: Pod) -> Pod:
        for i, p in enumerate(self._pods):
            if p.id == pod.id:
                self._pods[i] = pod
                return pod
        raise ValueError("Pod not found")

    def delete(self, pod_id: int) -> None:
        self._pods = [p for p in self._pods if p.id != pod_id]

    # === dùng bởi service/customer ===
    def exists(self, pod_id: int) -> bool:
        return any(p.id == pod_id for p in self._pods)

    def list_pods(self, page: int, limit: int, location_id: Optional[int]):
        pods = self._pods
        if location_id is not None:
            pods = [p for p in pods if getattr(p, "location_id", None) == int(location_id)]
        total = len(pods)
        start = (page - 1) * limit
        end = start + limit
        return [p.__dict__ for p in pods[start:end]], total
