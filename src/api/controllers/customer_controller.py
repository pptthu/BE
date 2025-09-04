from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, ValidationError
from datetime import datetime
from services.booking_service import BookingService
from infrastructure.repositories.booking_repository import BookingRepository
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
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    location_id = request.args.get("location_id")
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

    # giả sử đã có user_id từ JWT; demo hard-code  => thay bằng get_jwt() nếu anh đã cấu hình
    user_id = request.headers.get("X-Demo-UserId", 1)

    bk = booking_service.create_booking_for_customer(
        user_id=user_id,
        pod_id=payload["pod_id"],
        start_time=payload["start_time"],
        end_time=payload["end_time"],
    )
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
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    items, total = booking_service.list_customer_bookings(
        user_id=user_id, status=status, dt_from=dt_from, dt_to=dt_to, page=page, limit=limit
    )
    return jsonify({"items": resp_schema.dump(items, many=True), "total": total, "page": page, "limit": limit}), 200
