from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from src.infrastructure.models.pod_model import POD
from src.infrastructure.models.booking_model import Booking
from src.api.schemas.pod_schema import PODSchema

bp = Blueprint("pods", __name__)

@bp.get("/pods")
@jwt_required(optional=True)
def list_pods():
    location_id = request.args.get("location_id", type=int)
    start = request.args.get("from")
    end = request.args.get("to")

    q = POD.query
    if location_id:
        q = q.filter_by(location_id=location_id)
    pods = q.all()

    if not (start and end):
        return jsonify(PODSchema(many=True).dump(pods))

    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)
    result = []
    for p in pods:
        overlaps = (Booking.query.filter_by(pod_id=p.id)
                    .filter(Booking.end_time > start_dt, Booking.start_time < end_dt)
                    .all())
        available = all(b.status not in ("pending", "confirmed", "checked_in") for b in overlaps)
        data = PODSchema().dump(p)
        data["available"] = available
        result.append(data)
    return jsonify(result)

@bp.get("/pods/<int:pod_id>")
@jwt_required(optional=True)
def get_pod(pod_id):
    return jsonify(PODSchema().dump(POD.query.get_or_404(pod_id)))
