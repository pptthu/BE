from flask import Blueprint, request
from src.infrastructure.databases import get_session
from src.infrastructure.models.pod_model import PODModel
from src.api.schemas.pod import PODSchema
from src.api.responses import success_response
from src.services.pod_service import PodService

bp = Blueprint("pods", __name__, url_prefix="/pods")
schema = PODSchema()

@bp.get("/")
def list_pods():
    session = get_session()()
    location_id = request.args.get("location_id", type=int)
    q = session.query(PODModel)
    if location_id:
        q = q.filter(PODModel.location_id == location_id)
    return success_response(schema.dump(q.all(), many=True))

@bp.get("/<int:pod_id>")
def get_pod(pod_id: int):
    session = get_session()()
    pod = session.get(PODModel, pod_id)
    if not pod:
        return success_response(None, "Not found", 404)
    return success_response(schema.dump(pod))
