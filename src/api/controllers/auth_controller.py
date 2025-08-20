from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from src.infrastructure.databases.extensions import db
from src.infrastructure.models.user_model import User
from src.infrastructure.models.role_model import Role

bp = Blueprint("auth", __name__)

@bp.post("/register")
def register():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    full_name = data.get("full_name", "User")
    if not email or not password:
        return jsonify({"error": "bad_request", "message": "email and password are required"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "conflict", "message": "email already exists"}), 409

    role = Role.query.filter_by(name="customer").first()
    if not role:
        role = Role(name="customer")
        db.session.add(role); db.session.commit()

    u = User(email=email, full_name=full_name, role_id=role.id)
    u.set_password(password)
    db.session.add(u); db.session.commit()
    return jsonify({"id": u.id, "email": u.email}), 201

@bp.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    u = User.query.filter_by(email=email).first()
    if not u or not u.check_password(password) or not u.is_active:
        return jsonify({"error": "unauthorized", "message": "Invalid credentials"}), 401

    role_name = u.role.name if u.role else "customer"
    token = create_access_token(identity=str(u.id), additional_claims={
        "role": role_name, "user_id": u.id
    })
    return jsonify({
        "access_token": token,
        "role": role_name,
        "user": {"id": u.id, "full_name": u.full_name, "email": u.email,
                 "role_id": u.role_id, "location_id": u.location_id}
    })
