from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from src.infrastructure.databases.extensions import db
from src.infrastructure.models.user_model import User
from src.api.schemas.user_schema import UserSchema

bp = Blueprint("users", __name__)
user_schema = UserSchema()

@bp.get("/me/profile")
@jwt_required()
def me():
    uid = int(get_jwt().get("user_id"))
    return jsonify(user_schema.dump(User.query.get_or_404(uid)))

@bp.put("/me/profile")
@jwt_required()
def update_me():
    uid = int(get_jwt().get("user_id"))
    u = User.query.get_or_404(uid)
    data = request.get_json() or {}
    u.full_name = data.get("full_name", u.full_name)
    db.session.commit()
    return jsonify(user_schema.dump(u))

@bp.get("/me/bookings")
@jwt_required()
def my_bookings():
    from src.infrastructure.models.booking_model import Booking
    from src.api.schemas.booking_schema import BookingSchema
    uid = int(get_jwt().get("user_id"))
    q = Booking.query.filter_by(user_id=uid).order_by(Booking.created_at.desc())
    return jsonify(BookingSchema(many=True).dump(q.all()))
