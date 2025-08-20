from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime, date
from src.infrastructure.databases.extensions import db
from src.infrastructure.models.booking_model import Booking
from src.infrastructure.models.user_model import User
from src.api.schemas.booking_schema import BookingSchema
from src.api.middleware import roles_required

bp = Blueprint("staff", __name__)

@bp.get("/staff/bookings")
@jwt_required()
@roles_required("staff")
def staff_bookings():
    user_id = int(get_jwt().get("user_id"))
    staff = User.query.get_or_404(user_id)
    if not staff.location_id:
        return jsonify({"error": "forbidden", "message": "Staff has no assigned location"}), 403

    day_str = request.args.get("date")
    day = datetime.fromisoformat(day_str).date() if day_str else date.today()
    start_dt = datetime.combine(day, datetime.min.time())
    end_dt = datetime.combine(day, datetime.max.time())

    q = Booking.query.join(Booking.pod).filter(Booking.start_time >= start_dt, Booking.start_time <= end_dt)
    bookings = [b for b in q.all() if b.pod and b.pod.location_id == staff.location_id]
    return jsonify(BookingSchema(many=True).dump(bookings))

@bp.put("/staff/bookings/<int:booking_id>/checkin")
@jwt_required()
@roles_required("staff")
def checkin(booking_id):
    staff = User.query.get_or_404(int(get_jwt().get("user_id")))
    booking = Booking.query.get_or_404(booking_id)
    if not booking.pod or booking.pod.location_id != staff.location_id:
        return jsonify({"error": "forbidden", "message": "Different location"}), 403
    if booking.status not in ("confirmed",):
        return jsonify({"error": "bad_request", "message": "Booking must be confirmed before check-in"}), 400

    booking.status = "checked_in"
    db.session.commit()
    return jsonify({"id": booking.id, "status": booking.status})

@bp.put("/staff/bookings/<int:booking_id>/checkout")
@jwt_required()
@roles_required("staff")
def checkout(booking_id):
    staff = User.query.get_or_404(int(get_jwt().get("user_id")))
    booking = Booking.query.get_or_404(booking_id)
    if not booking.pod or booking.pod.location_id != staff.location_id:
        return jsonify({"error": "forbidden", "message": "Different location"}), 403
    if booking.status not in ("checked_in",):
        return jsonify({"error": "bad_request", "message": "Booking must be checked_in before check-out"}), 400

    booking.status = "checked_out"
    db.session.commit()
    return jsonify({"id": booking.id, "status": booking.status})
