from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from src.infrastructure.databases.extensions import db
from src.api.middleware import roles_required
from src.infrastructure.models.user_model import User
from src.infrastructure.models.role_model import Role

bp = Blueprint("admin", __name__)

@bp.get("/admin/users")
@jwt_required()
@roles_required("admin")
def list_users():
    users = User.query.all()
    return jsonify([{
        "id": u.id,
        "full_name": u.full_name,
        "email": u.email,
        "role_id": u.role_id,
        "role_name": u.role.name if u.role else None,
        "is_active": u.is_active,
        "location_id": u.location_id
    } for u in users])

@bp.post("/admin/users")
@jwt_required()
@roles_required("admin")
def create_user():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password") or "Aa@123456"
    full_name = data.get("full_name", "User")
    role_name = data.get("role", "customer")

    role = Role.query.filter_by(name=role_name).first()
    if not role:
        role = Role(name=role_name)
        db.session.add(role); db.session.commit()

    u = User(email=email, full_name=full_name, role_id=role.id, location_id=data.get("location_id"))
    u.set_password(password)
    db.session.add(u); db.session.commit()
    return jsonify({"id": u.id}), 201

@bp.put("/admin/users/<int:user_id>")
@jwt_required()
@roles_required("admin")
def update_user(user_id):
    u = User.query.get_or_404(user_id)
    data = request.get_json() or {}
    if "full_name" in data: u.full_name = data["full_name"]
    if "email" in data: u.email = data["email"]
    if "password" in data and data["password"]: u.set_password(data["password"])
    if "role" in data:
        role = Role.query.filter_by(name=data["role"]).first()
        if not role:
            role = Role(name=data["role"]); db.session.add(role); db.session.commit()
        u.role_id = role.id
    if "is_active" in data: u.is_active = bool(data["is_active"])
    if "location_id" in data: u.location_id = data["location_id"]
    db.session.commit()
    return jsonify({"id": u.id})

@bp.delete("/admin/users/<int:user_id>")
@jwt_required()
@roles_required("admin")
def delete_user(user_id):
    u = User.query.get_or_404(user_id)
    from src.infrastructure.models.booking_model import Booking
    if Booking.query.filter_by(user_id=u.id).first():
        return jsonify({"error": "conflict", "message": "User has bookings; disable instead"}), 409
    u.is_active = False
    db.session.commit()
    return jsonify({"disabled": True})
