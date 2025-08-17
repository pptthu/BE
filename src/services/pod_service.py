from decimal import Decimal
from typing import List, Optional
from sqlalchemy import and_
from src.infrastructure.models.pod_model import PODModel

class PodService:
    @staticmethod
    def create(session, name: str, price: float | Decimal, status: str, location_id: int) -> PODModel:
        exists = (session.query(PODModel)
                  .filter(and_(PODModel.name == name, PODModel.location_id == location_id))
                  .first())
        if exists: raise ValueError("POD name already exists in this location.")
        pod = PODModel(name=name, price=Decimal(price), status=status, location_id=location_id)
        session.add(pod); session.commit(); session.refresh(pod); return pod

    @staticmethod
    def update(session, pod_id: int, **fields) -> PODModel:
        pod: Optional[PODModel] = session.get(PODModel, pod_id)
        if not pod: raise LookupError("POD not found")
        for k, v in fields.items():
            if hasattr(pod, k) and v is not None:
                setattr(pod, k, v)
        session.commit(); session.refresh(pod); return pod

    @staticmethod
    def update_status(session, pod_id: int, status: str) -> PODModel:
        return PodService.update(session, pod_id, status=status)

    @staticmethod
    def list_all(session) -> List[PODModel]:
        return session.query(PODModel).order_by(PODModel.id.asc()).all()

    @staticmethod
    def list_available_by_location(session, location_id: int) -> List[PODModel]:
        return (session.query(PODModel)
                .filter(PODModel.location_id == location_id, PODModel.status == "available")
                .order_by(PODModel.id.asc()).all())
