from flask import Blueprint
from src.api.responses import success_response

bp = Blueprint("staff", __name__, url_prefix="/staff")

@bp.get("/bookings/today")
def bookings_today():
    # Placeholder - implement a real query for today's bookings
    return success_response([], "Staff - today's bookings")
