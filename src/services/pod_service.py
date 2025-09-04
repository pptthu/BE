from infrastructure.models.pod_model import PodModel
from infrastructure.databases.mssql import session
from datetime import datetime

class PodService:
    def list_pods(self):
        return session.query(PodModel).all()

    def get_pod(self, pod_id):
        return session.query(PodModel).get(pod_id)

    def create_pod(self, data):
        pod = PodModel(
            code=data["code"],
            name=data["name"],
            status=data.get("status", "active"),
            location_id=data["location_id"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(pod)
        session.commit()
        return pod

    def update_pod(self, pod_id, data):
        pod = session.query(PodModel).get(pod_id)
        if not pod:
            return None
        pod.code = data.get("code", pod.code)
        pod.name = data.get("name", pod.name)
        pod.status = data.get("status", pod.status)
        pod.location_id = data.get("location_id", pod.location_id)
        pod.updated_at = datetime.utcnow()
        session.commit()
        return pod

    def delete_pod(self, pod_id):
        pod = session.query(PodModel).get(pod_id)
        if pod:
            session.delete(pod)
            session.commit()
