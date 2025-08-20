from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime
from src.infrastructure.databases.extensions import db
from src.infrastructure.models.booking_model import Booking
from src.infrastructure.models.pod_model import POD
from src.api.schemas.booking_schema import BookingSchema
from src.services.booking_service import calc_price, ensure_not_overlap, attach_services

bp = Blueprint("bookings", __name__)

@bp.post("/bookings")
@jwt_required()
def create_booking():
    data = request.get_json() or {}
    pod_id = data.get("pod_id")
    start_time = data.get("start_time")
    end_time = data.get("end_time")
    services = data.get("services", [])
    if not pod_id or not start_time or not end_time:
        return jsonify({"error": "bad_request", "message": "pod_id, start_time, end_time required"}), 400

    start_dt = datetime.fromisoformat(start_time)
    end_dt = datetime.fromisoformat(end_time)
    if end_dt <= start_dt:
        return jsonify({"error": "bad_request", "message": "end_time must be after start_time"}), 400

    pod = POD.query.get_or_404(pod_id)
    if not ensure_not_overlap(pod_id, start_dt, end_dt):
        return jsonify({"error": "conflict", "message": "Time range overlaps with existing booking"}), 409

    total = calc_price(pod, start_dt, end_dt, services)
    booking = Booking(
        user_id=int(get_jwt().get("user_id")),
        pod_id=pod_id,
        start_time=start_dt,
        end_time=end_dt,
        total_price=total,
        status="pending",
        payment_status="unpaid",
    )
    db.session.add(booking)
    db.session.flush()  # để có booking.id
    attach_services(booking.id, services)
    db.session.commit()
    return jsonify(BookingSchema().dump(booking)), 201

@bp.post("/bookings/<int:booking_id>/confirm-payment")
@jwt_required()
def confirm_payment(booking_id):
    uid = int(get_jwt().get("user_id"))
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != uid:
        return jsonify({"error": "forbidden", "message": "Not your booking"}), 403
    if booking.payment_status == "paid":
        return jsonify(BookingSchema().dump(booking))

    booking.payment_status = "paid"
    booking.status = "confirmed"
    booking.payment_confirmed_at = datetime.utcnow()
    db.session.commit()

    # Giả lập thông báo
    print(f"[NOTIFY] Booking {booking.id} has been PAID by user {uid}.")
    return jsonify(BookingSchema().dump(booking))
