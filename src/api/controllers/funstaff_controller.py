# src/api/controllers/funstaff_controller.py
from flask import Blueprint, request, jsonify
from datetime import datetime
from services.booking_staffcus_service import BookingService
from infrastructure.repositories.booking_staff_repository import BookingRepository
from api.schemas.booking_staff_schema import BookingResponseSchema
from infrastructure.repositories.pod_cus_repository import PodRepository
from infrastructure.repositories.user_cus_repository import UserRepository

bp = Blueprint("staff", __name__, url_prefix="/staff")

booking_service = BookingService(
    booking_repo=BookingRepository(),
    pod_repo=PodRepository(),
    user_repo=UserRepository(),
)
resp_schema = BookingResponseSchema()

@bp.route("/bookings", methods=["GET"])
def staff_list_bookings():
    """
    ---
    get:
      tags: [Staff]
      summary: List staff bookings with optional filters
      parameters:
        - in: query
          name: status
          schema: { type: string }
        - in: query
          name: user_id
          schema: { type: integer }
        - in: query
          name: pod_id
          schema: { type: integer }
        - in: query
          name: from
          schema: { type: string, format: date-time }
        - in: query
          name: to
          schema: { type: string, format: date-time }
        - in: query
          name: page
          schema: { type: integer, minimum: 1 }
        - in: query
          name: limit
          schema: { type: integer, minimum: 1, maximum: 100 }
      responses:
        200: { description: OK }
    """
    status = (request.args.get("status") or "").strip() or None
    user_id = request.args.get("user_id", type=int)
    user_name = request.args.get("user_name", type=str)
    pod_id  = request.args.get("pod_id",  type=int)
    dt_from = request.args.get("from")
    dt_to   = request.args.get("to")
    page    = request.args.get("page", default=1, type=int)
    limit   = request.args.get("limit", default=20, type=int)

    items, total = booking_service.list_staff_bookings(
        status=status, user_id=user_id, pod_id=pod_id,
        dt_from=dt_from, dt_to=dt_to, page=page, limit=limit
    )
    return jsonify({
        "items": resp_schema.dump(items, many=True),
        "total": total, "page": page, "limit": limit
    }), 200

@bp.route("/bookings/<int:booking_id>/checkin", methods=["POST"])
def staff_checkin(booking_id: int):
    """
    ---
    post:
      tags: [Staff]
      summary: Staff check-in booking
      parameters:
        - in: path
          name: booking_id
          required: true
          schema: { type: integer }
        - in: query
          name: at
          required: false
          schema: { type: string, format: date-time }
          description: Optional override for check-in time (ISO-8601)
      requestBody:
        required: false
        content:
          application/json:
            schema:
              type: object
              properties:
                at:
                  type: string
                  format: date-time
                  description: Optional override for check-in time (ISO-8601)
      responses:
        200: { description: Checked-in }
        400: { description: Bad request }
        404: { description: Not found }
    """
    body = request.get_json(silent=True) or {}
    at = body.get("at")
    at_dt = None
    if at:
        try:
            at_dt = datetime.fromisoformat(at)
        except Exception:
            return jsonify({"error": "Thời gian 'at' phải là ISO 8601"}), 400

    try:
        b = booking_service.check_in(booking_id, at_time=at_dt)
    except ValueError as e:
        msg = str(e)
        if msg.lower() == "booking not found":
            return jsonify({"error": msg}), 404
        return jsonify({"error": msg}), 400

    return jsonify(resp_schema.dump(b)), 200

@bp.route("/bookings/<int:booking_id>/checkout", methods=["POST"])
def staff_checkout(booking_id: int):
    """
    ---
    post:
      tags: [Staff]
      summary: Staff check-out booking
      parameters:
        - in: path
          name: booking_id
          required: true
          schema: { type: integer }
        - in: query
          name: at
          required: false
          schema: { type: string, format: date-time }
          description: Optional override for check-out time (ISO-8601)
      requestBody:
        required: false
        content:
          application/json:
            schema:
              type: object
              properties:
                at:
                  type: string
                  format: date-time
                  description: Optional override for check-out time (ISO-8601)
      responses:
        200: { description: Checked-out }
        400: { description: Bad request }
        404: { description: Not found }
    """
    body = request.get_json(silent=True) or {}
    at = body.get("at")
    at_dt = None
    if at:
        try:
            at_dt = datetime.fromisoformat(at)
        except Exception:
            return jsonify({"error": "Thời gian 'at' phải là ISO 8601"}), 400

    try:
        b = booking_service.check_out(booking_id, at_time=at_dt)
    except ValueError as e:
        msg = str(e)
        if msg.lower() == "booking not found":
            return jsonify({"error": msg}), 404
        return jsonify({"error": msg}), 400

    return jsonify(resp_schema.dump(b)), 200
