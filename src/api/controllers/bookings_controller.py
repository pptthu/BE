from flask import Blueprint, request, g, current_app, send_file, url_for
from ..middleware import auth_required
from ...services.booking_service import BookingService
from ..responses import ok, fail
from ..schemas.booking import CreateBookingRequest
import os

bp = Blueprint("bookings", __name__)

@bp.post("/bookings")
@auth_required
def create_booking():
    data = request.get_json(silent=True) or {}
    errors = CreateBookingRequest().validate(data)
    if errors:
        return fail(str(errors), 400)
    svc = BookingService(g.db)
    try:
        booking = svc.create_booking(
            user_id=request.user["id"],
            pod_id=data["pod_id"],
            start_time=data["start_time"],
            end_time=data["end_time"],
        )
        return ok(booking, 201)
    except Exception as e:
        g.db.rollback()
        return fail(str(e), 400)

@bp.get("/bookings")
@auth_required
def list_my_bookings():
    svc = BookingService(g.db)
    items = svc.list_my_bookings(user_id=request.user["id"])
    return ok(items)

@bp.get("/bookings/<int:booking_id>")
@auth_required
def get_booking(booking_id: int):
    svc = BookingService(g.db)
    b = svc.get(booking_id, owner_id=request.user["id"])
    if not b:
        return fail("Not found", 404)
    return ok(b)

@bp.get("/bookings/<int:booking_id>/payment")
@auth_required
def get_booking_payment(booking_id: int):
    svc = BookingService(g.db)
    b = svc.get(booking_id, owner_id=request.user["id"])
    if not b:
        return fail("Not found", 404)
    b["qr_url"] = url_for("bookings.get_qr", _external=True)
    return ok(b)

@bp.post("/bookings/<int:booking_id>/confirm-payment")
@auth_required
def confirm_payment(booking_id: int):
    svc = BookingService(g.db)
    try:
        booking = svc.confirm_payment(user_id=request.user["id"], booking_id=booking_id)
        return ok(booking)
    except Exception as e:
        g.db.rollback()
        return fail(str(e), 400)

@bp.get("/payment/qr")
def get_qr():
    path = current_app.config.get("PAYMENT_QR_PATH", "./static/qr/qr.png")
    if not os.path.exists(path):
        return fail("QR image not found", 404)
    return send_file(path, mimetype="image/png")
