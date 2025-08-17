# src/api/controllers/bookings_controller.py
from flask import Blueprint, request, jsonify
from datetime import datetime
from marshmallow import ValidationError

from services.booking_service import BookingService
from infrastructure.repositories.booking_repository import BookingRepository
from api.schemas.booking import BookingRequestSchema, BookingResponseSchema
from api.schemas.booking_filters import BookingFilterQuerySchema
from api.schemas.booking_actions import (
    BookingConfirmSchema,
    BookingCancelSchema,
    BookingCheckinSchema,
    BookingCheckoutSchema
)

bp = Blueprint('bookings', __name__, url_prefix='/bookings')

booking_service = BookingService(BookingRepository())
request_schema = BookingRequestSchema()
response_schema = BookingResponseSchema()
filter_schema = BookingFilterQuerySchema()

confirm_schema = BookingConfirmSchema()
cancel_schema = BookingCancelSchema()
checkin_schema = BookingCheckinSchema()
checkout_schema = BookingCheckoutSchema()


# ------------------------- LIST + FILTER -------------------------
@bp.route('/', methods=['GET'])
def list_bookings():
    """
    GET /bookings?status=&user_id=&pod_id=&date_from=&date_to=&page=&limit=&sort_by=&sort_dir=
    """
    try:
        # validate & parse query params
        params = filter_schema.load(request.args)
    except ValidationError as err:
        return jsonify(err.messages), 400

    items = booking_service.list_bookings()

    # --- filter ---
    status = params.get('status')
    user_id = params.get('user_id')
    pod_id = params.get('pod_id')
    date_from = params.get('date_from')
    date_to = params.get('date_to')

    if status:
        items = [b for b in items if getattr(b, 'status', None) == status]
    if user_id:
        items = [b for b in items if getattr(b, 'user_id', None) == user_id]
    if pod_id:
        items = [b for b in items if getattr(b, 'pod_id', None) == pod_id]
    if date_from:
        items = [b for b in items if getattr(b, 'start_time', None) and b.start_time >= date_from]
    if date_to:
        items = [b for b in items if getattr(b, 'end_time', None) and b.end_time <= date_to]

    # --- sort ---
    sort_by = params.get('sort_by', 'start_time')
    sort_dir = params.get('sort_dir', 'desc')
    try:
        items.sort(key=lambda x: getattr(x, sort_by, None), reverse=(sort_dir == 'desc'))
    except Exception:
        # nếu sort field không tồn tại thì bỏ qua
        pass

    # --- paging ---
    page = params.get('page', 1)
    limit = params.get('limit', 20)
    total = len(items)
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    page_items = items[start_idx:end_idx]

    return jsonify({
        "items": response_schema.dump(page_items, many=True),
        "page": page,
        "limit": limit,
        "total": total
    }), 200


# ------------------------- GET ONE -------------------------
@bp.route('/<int:booking_id>', methods=['GET'])
def get_booking(booking_id: int):
    booking = booking_service.get_booking(booking_id)
    if not booking:
        return jsonify({'message': 'Booking not found'}), 404
    return jsonify(response_schema.dump(booking)), 200


# ------------------------- CREATE -------------------------
@bp.route('/', methods=['POST'])
def create_booking():
    data = request.get_json() or {}
    try:
        payload = request_schema.load(data)  # parse & cast DateTime
    except ValidationError as err:
        return jsonify(err.messages), 400

    now = datetime.utcnow()
    booking = booking_service.create_booking(
        user_id=payload['user_id'],
        pod_id=payload['pod_id'],
        start_time=payload['start_time'],
        end_time=payload['end_time'],
        status=payload.get('status', 'CONFIRMED'),
        created_at=now,
        updated_at=now
    )
    return jsonify(response_schema.dump(booking)), 201


# ------------------------- UPDATE (full) -------------------------
@bp.route('/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id: int):
    data = request.get_json() or {}
    try:
        payload = request_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    booking = booking_service.update_booking(
        booking_id=booking_id,
        user_id=payload['user_id'],
        pod_id=payload['pod_id'],
        start_time=payload['start_time'],
        end_time=payload['end_time'],
        status=payload.get('status', 'CONFIRMED'),
        created_at=None,  # service sẽ giữ nguyên created_at hiện có
        updated_at=datetime.utcnow()
    )
    return jsonify(response_schema.dump(booking)), 200


# ------------------------- DELETE -------------------------
@bp.route('/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id: int):
    ok = booking_service.delete_booking(booking_id)
    if not ok:
        return jsonify({'message': 'Booking not found'}), 404
    return '', 204


# ========================= ACTIONS: CONFIRM/CANCEL/CHECKIN/CHECKOUT =========================
def _set_status(booking_id: int, new_status: str):
    """Helper: đổi status bằng cách lấy booking hiện tại rồi update."""
    current = booking_service.get_booking(booking_id)
    if not current:
        return None
    updated = booking_service.update_booking(
        booking_id=booking_id,
        user_id=current.user_id,
        pod_id=current.pod_id,
        start_time=current.start_time,
        end_time=current.end_time,
        status=new_status,
        created_at=current.created_at,
        updated_at=datetime.utcnow()
    )
    return updated


@bp.route('/<int:booking_id>/confirm', methods=['POST'])
def confirm_booking(booking_id: int):
    data = request.get_json(silent=True) or {}
    try:
        confirm_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    updated = _set_status(booking_id, "CONFIRMED")
    if not updated:
        return jsonify({'message': 'Booking not found'}), 404
    return jsonify(response_schema.dump(updated)), 200


@bp.route('/<int:booking_id>/cancel', methods=['POST'])
def cancel_booking(booking_id: int):
    data = request.get_json(silent=True) or {}
    try:
        cancel_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    updated = _set_status(booking_id, "CANCELLED")
    if not updated:
        return jsonify({'message': 'Booking not found'}), 404
    return jsonify(response_schema.dump(updated)), 200


@bp.route('/<int:booking_id>/checkin', methods=['POST'])
def checkin_booking(booking_id: int):
    data = request.get_json(silent=True) or {}
    try:
        checkin_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    updated = _set_status(booking_id, "CHECKED_IN")
    if not updated:
        return jsonify({'message': 'Booking not found'}), 404
    return jsonify(response_schema.dump(updated)), 200


@bp.route('/<int:booking_id>/checkout', methods=['POST'])
def checkout_booking(booking_id: int):
    data = request.get_json(silent=True) or {}
    try:
        checkout_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    updated = _set_status(booking_id, "CHECKED_OUT")
    if not updated:
        return jsonify({'message': 'Booking not found'}), 404
    return jsonify(response_schema.dump(updated)), 200
