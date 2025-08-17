from flask import Blueprint, request, jsonify
from datetime import datetime
from marshmallow import ValidationError

from services.auth_service import AuthService
from infrastructure.repositories.user_repository import UserRepository
from api.schemas.user import (
    UserCreateRequestSchema,
    UserChangePasswordRequestSchema,
)
# Giả định anh đã có file schemas/auth.py với schema login
# Nếu chưa có, tạo nhanh AuthLoginRequestSchema(email/username + password)
from api.schemas.auth import AuthLoginRequestSchema

bp = Blueprint("auth", __name__, url_prefix="/auth")

auth_service = AuthService(UserRepository())

register_schema = UserCreateRequestSchema()
login_schema = AuthLoginRequestSchema()
change_pw_schema = UserChangePasswordRequestSchema()


@bp.route("/register", methods=["POST"])
def register():
    """
    POST /auth/register
    Body: dùng lại UserCreateRequestSchema
    {
      "username": "...",
      "email": "...",
      "password": "...",
      "roles_id": 2
    }
    """
    data = request.get_json() or {}
    try:
        payload = register_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    now = datetime.utcnow()
    user = auth_service.register(
        username=payload["username"],
        email=payload["email"],
        password=payload["password"],
        roles_id=payload["roles_id"],
        created_at=now,
        updated_at=now,
    )
    # trả về thông tin cơ bản
    return jsonify({
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "roles_id": user.roles_id,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None,
    }), 201


@bp.route("/login", methods=["POST"])
def login():
    """
    POST /auth/login
    Body (ví dụ):
    {
      "username": "kiet",
      "password": "123456"
    }
    """
    data = request.get_json() or {}
    try:
        payload = login_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    info = auth_service.login(payload["username"], payload["password"])
    if not info:
        return jsonify({"message": "Invalid credentials"}), 401
    return jsonify(info), 200


@bp.route("/change-password", methods=["POST"])
def change_password():
    """
    POST /auth/change-password
    Body:
    {
      "user_id": 1,
      "old_password": "...",
      "new_password": "..."
    }
    """
    data = request.get_json() or {}
    try:
        payload = change_pw_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"user_id": ["Missing data for required field."]}), 400

    ok = auth_service.change_password(user_id, payload["old_password"], payload["new_password"])
    if not ok:
        return jsonify({"message": "Invalid user or password"}), 400
    return jsonify({"message": "Password changed"}), 200
