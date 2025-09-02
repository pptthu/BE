from flask import Blueprint, request, jsonify, session
from app import db
from infrastructure.models.user_model import User
from schemas.user import LoginSchema
from services.admin_service import AdminService

bp = Blueprint("admin", __name__)

@bp.post("/admin/login")
def login():
    data = request.get_json() or {}
    schema = LoginSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    email, password = data["email"], data["password"]
    user = AdminService.login(email, password)

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    session["user_id"] = user.id
    session["role"] = user.role

    return jsonify({
        "msg": "Login successful",
        "user": {"id": user.id, "email": user.email, "role": user.role}
    })


@bp.post("/admin/logout")
def logout():
    session.clear()
    return jsonify({"msg": "Logged out successfully"})


@bp.get("/admin/users")
def get_users():
    if session.get("role") != "Admin":
        return jsonify({"error": "Forbidden"}), 403

    users = User.query.all()
    return jsonify([
        {"id": u.id, "email": u.email, "role": u.role}
        for u in users
    ])


@bp.post("/admin/users")
def create_user():
    if session.get("role") != "Admin":
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json() or {}
    try:
        user = User(
            email=data["email"],
            role=data.get("role", "Customer")
        )
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()
        return jsonify({"msg": "User created", "id": user.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@bp.put("/admin/users/<int:user_id>")
def update_user(user_id):
    if session.get("role") != "Admin":
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json() or {}
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.email = data.get("email", user.email)
    if "password" in data:
        user.set_password(data["password"])
    if "role" in data:
        user.role = data["role"]

    db.session.commit()
    return jsonify({"msg": "User updated"})


@bp.delete("/admin/users/<int:user_id>")
def delete_user(user_id):
    if session.get("role") != "Admin":
        return jsonify({"error": "Forbidden"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted"})


@bp.put("/admin/users/<int:user_id>/role")
def assign_role(user_id):
    if session.get("role") != "Admin":
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json() or {}
    new_role = data.get("role")
    if not new_role:
        return jsonify({"error": "Role is required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.role = new_role
    db.session.commit()
    return jsonify({"msg": f"User role updated to {new_role}"})
