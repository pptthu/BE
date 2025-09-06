from flask import Blueprint, g
from ..middleware import auth_required, roles_required
from ...services.staff_service import StaffService
from ..responses import ok, fail

bp = Blueprint("staff", __name__)

@bp.get("/staff/bookings")
@auth_required
@roles_required("STAFF", "MANAGER", "ADMIN")
def staff_list_bookings():
    svc = StaffService(g.db)
    return ok(svc.list_bookings())

@bp.put("/staff/bookings/<int:booking_id>/checkin")
@auth_required
@roles_required("STAFF", "MANAGER", "ADMIN")
def checkin(booking_id: int):
    svc = StaffService(g.db)
    try:
        data = svc.checkin(booking_id)
        return ok(data)
    except Exception as e:
        g.db.rollback()
        return fail(str(e), 400)

@bp.put("/staff/bookings/<int:booking_id>/checkout")
@auth_required
@roles_required("STAFF", "MANAGER", "ADMIN")
def checkout(booking_id: int):
    svc = StaffService(g.db)
    try:
        data = svc.checkout(booking_id)
        return ok(data)
    except Exception as e:
        g.db.rollback()
        return fail(str(e), 400)
