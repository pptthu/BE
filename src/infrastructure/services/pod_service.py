# src/infrastructure/services/pod_service.py
from src.infrastructure.repositories.pod_repository import PodRepository

class PodService:
    def __init__(self, repo: PodRepository): self.repo = repo
    def list_pods(self, location_id: int|None=None):
        return self.repo.list(location_id)
