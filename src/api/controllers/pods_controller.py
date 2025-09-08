from flask import Blueprint, request, g
from ...services.pods_service import PodsService
from ..responses import ok, fail

bp = Blueprint("pods", __name__)

@bp.get("/pods")
def list_pods():
    """
    Query:
      - location_id (int, optional)
      - start_time, end_time (ISO 8601, optional): nếu có, chỉ trả POD rảnh trong khoảng này
    """
    q_loc = request.args.get("location_id")
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")

    svc = PodsService(g.db)
    pods = svc.list_pods(
        location_id=int(q_loc) if q_loc else None,
        start_time=start_time,
        end_time=end_time
    )
    return ok(pods)

@bp.get("/pods/<int:pod_id>")
def get_pod(pod_id: int):
    svc = PodsService(g.db)
    pod = svc.get_pod(pod_id)
    if not pod:
        return fail("Not found", 404)
    return ok(pod)
