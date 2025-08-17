from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.infrastructure.databases import get_session
from src.infrastructure.models.booking_model import BookingModel
from src.infrastructure.models.booking_service_model import BookingService
from src.api.schemas.booking import BookingSchema
from src.api.responses import success_response, error_response
from src.services.booking_service import BookingService

bp = Blueprint("booking", __name__, url_prefix="/bookings")
schema = BookingSchema()

@bp.post("/")
@jwt_required()
def create_booking():
    payload = request.json or {}
    for f in ("pod_id", "start_time", "end_time"):
        if f not in payload:
            return error_response(f"Missing field: {f}", 400)

    session = get_session()()
    ident = get_jwt_identity() or {}
    user_id = ident.get("user_id")

    try:
        booking = BookingService.create_booking(
            session=session,
            user_id=int(user_id),
            pod_id=int(payload["pod_id"]),
            start_iso=str(payload["start_time"]),
            end_iso=str(payload["end_time"]),
            status="pending",
        )
    except ValueError as ve:
        return error_response(str(ve), 400)
    except LookupError as le:
        return error_response(str(le), 404)

    return success_response(schema.dump(booking), "Booking created", 201)

@bp.post("/<int:booking_id>/confirm")
@jwt_required()
def confirm_booking(booking_id: int):
    session = get_session()()
    try:
        booking = BookingService.confirm_booking(session, booking_id)
    except LookupError as le:
        return error_response(str(le), 404)
    return success_response(schema.dump(booking), "Booking confirmed")

@bp.get("/")
@jwt_required(optional=True)
def list_bookings():
    session = get_session()()
    rows = session.query(BookingModel).order_by(BookingModel.id.desc()).all()
    return success_response(schema.dump(rows, many=True))
