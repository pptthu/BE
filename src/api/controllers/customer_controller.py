# src/api/controllers/customer_controller.py
from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, ValidationError
from services.booking_staffcus_service import BookingService
from infrastructure.repositories.booking_staff_repository import BookingRepository
from infrastructure.repositories.pod_cus_repository import PodRepository
from infrastructure.repositories.user_cus_repository import UserRepository

bp = Blueprint("customer", __name__, url_prefix="/customer")

# ====== Schemas ======
class BookingCreateSchema(Schema):
    pod_id = fields.Int(required=True)
    start_time = fields.DateTime(required=True)  # ISO 8601
    end_time = fields.DateTime(required=True)

class BookingRespSchema(Schema):
    id = fields.Int()
    pod_id = fields.Int()
    user_id = fields.Int()
    status = fields.Str()
    start_time = fields.DateTime()
    end_time = fields.DateTime()
    created_at = fields.DateTime()
    total_price = fields.Float(allow_none=True)

create_schema = BookingCreateSchema()
resp_schema = BookingRespSchema()

booking_service = BookingService(
    booking_repo=BookingRepository(),
    pod_repo=PodRepository(),
    user_repo=UserRepository(),
)

@bp.get("/pods")
def list_pods():
    """
    ---
    get:
      tags: [Customer]
      summary: List PODs
      parameters:
        - in: query
          name: page
          schema: {type: integer, minimum: 1}
        - in: query
          name: limit
          schema: {type: integer, minimum: 1, maximum: 100}
        - in: query
          name: location_id
          schema: {type: integer}
      responses:
        200:
          description: OK
    """
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)
    location_id = request.args.get("location_id", type=int)
    pods, total = booking_service.list_pods(page, limit, location_id)
    return jsonify({"items": pods, "total": total, "page": page, "limit": limit}), 200

@bp.post("/bookings")
def create_booking():
    """
    ---
    post:
      tags: [Customer]
      summary: Create a booking
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                pod_id: { type: integer }
                start_time: { type: string, format: date-time }
                end_time: { type: string, format: date-time }
      responses:
        201: { description: Created }
        400: { description: Bad request }
        409: { description: Time slot conflicts }
    """
    try:
        payload = create_schema.load(request.get_json() or {})
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400

    # demo: dùng header giả lập; sau này thay bằng get_jwt_identity()
    user_id = int(request.headers.get("X-Demo-UserId", 1))

    try:
        bk = booking_service.create_booking_for_customer(
            user_id=user_id,
            pod_id=payload["pod_id"],
            start_time=payload["start_time"],
            end_time=payload["end_time"],
        )
    except ValueError as e:
        msg = str(e)
        if msg == "Time slot conflicts":
            return jsonify({"error": msg}), 409
        return jsonify({"error": msg}), 400

    return jsonify(resp_schema.dump(bk)), 201

@bp.get("/profile")
def get_profile():
    """
    ---
    get:
      tags: [Customer]
      summary: Get customer profile
      responses:
        200: { description: OK }
    """
    user_id = int(request.headers.get("X-Demo-UserId", 1))
    profile = booking_service.get_customer_profile(user_id)
    return jsonify(profile), 200

@bp.get("/bookings")
def customer_history():
    """
    ---
    get:
      tags: [Customer]
      summary: Booking history
      parameters:
        - in: query
          name: status
          schema: { type: string }
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
    user_id = int(request.headers.get("X-Demo-UserId", 1))
    status = request.args.get("status")
    dt_from = request.args.get("from")
    dt_to = request.args.get("to")
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)

    items, total = booking_service.list_customer_bookings(
        user_id=user_id, status=status, dt_from=dt_from, dt_to=dt_to, page=page, limit=limit
    )
    return jsonify({"items": resp_schema.dump(items, many=True), "total": total, "page": page, "limit": limit}), 200
