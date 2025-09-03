from flask import Blueprint, request, jsonify
from datetime import datetime
from services.booking_service import BookingService
from infrastructure.repositories.booking_repository import BookingRepository
from api.schemas.booking_staff_schema import BookingResponseSchema

bp = Blueprint("staffs", __name__, url_prefix="/api/staff")

booking_service = BookingService(BookingRepository())
resp_schema = BookingResponseSchema()

# 1) Danh sách booking
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
      responses:
        200:
          description: OK
    """
    date = request.args.get("date")  # yyyy-mm-dd
    items = booking_service.list_bookings(date)
    # items là list [(BookingModel, customer_name)]
    result = []
    for booking, customer_name in items:
        data = resp_schema.dump(booking)
        data["customer_name"] = customer_name
        result.append(data)
    return jsonify(result), 200


# 2) Check-in
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
      responses:
        200: { description: Checked-in }
        400: { description: Bad request }
        404: { description: Not found }
    """
    data = request.get_json(silent=True) or {}
    at = data.get("at")
    at_dt = None
    if at:
        try:
            at_dt = datetime.fromisoformat(at)
        except Exception:
            return jsonify({"error": "Thời gian 'at' phải là ISO 8601"}), 400

    try:
        booking = booking_service.check_in(booking_id, at_time=at_dt)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(resp_schema.dump(booking)), 200


# 3) Check-out
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
      responses:
        200: { description: Checked-out }
        400: { description: Bad request }
        404: { description: Not found }
    """
    data = request.get_json(silent=True) or {}
    at = data.get("at")
    at_dt = None
    if at:
        try:
            at_dt = datetime.fromisoformat(at)
        except Exception:
            return jsonify({"error": "Thời gian 'at' phải là ISO 8601"}), 400

    try:
        booking = booking_service.check_out(booking_id, at_time=at_dt)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(resp_schema.dump(booking)), 200
