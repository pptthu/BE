# src/api/controllers/staff_controller.py
from flask import Blueprint, request, jsonify
from datetime import datetime
from marshmallow import ValidationError

from services.user_service import UserService
from infrastructure.repositories.user_repository import UserRepository
from api.schemas.user import (
    UserCreateRequestSchema,
    UserUpdateRequestSchema,
    UserResponseSchema,
)

bp = Blueprint("staffs", __name__, url_prefix="/staffs")

user_service = UserService(UserRepository())
create_schema = UserCreateRequestSchema()
update_schema = UserUpdateRequestSchema()
response_schema = UserResponseSchema()

# Đặt đúng ID role "staff" theo bảng roles của anh (ví dụ 2)
STAFF_ROLE_ID = 2


@bp.route("/", methods=["GET"])
def list_staffs():
    """GET /staffs - liệt kê user có role = staff"""
    all_users = user_service.list_users()
    staffs = [u for u in all_users if getattr(u, "roles_id", None) == STAFF_ROLE_ID]
    return jsonify(response_schema.dump(staffs, many=True)), 200


@bp.route("/<int:user_id>", methods=["GET"])
def get_staff(user_id: int):
    """GET /staffs/<id> - lấy chi tiết 1 staff"""
    u = user_service.get_user(user_id)
    if not u or getattr(u, "roles_id", None) != STAFF_ROLE_ID:
        return jsonify({"message": "Staff not found"}), 404
    return jsonify(response_schema.dump(u)), 200


@bp.route("/", methods=["POST"])
def create_staff():
    """
    POST /staffs
    Body theo UserCreateRequestSchema:
    {
      "username": "...",
      "email": "...",
      "password": "..."
      // roles_id sẽ bị ép = STAFF_ROLE_ID
    }
    """
    data = request.get_json() or {}
    try:
        payload = create_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    now = datetime.utcnow()
    staff = user_service.create_user(
        username=payload["username"],
        email=payload["email"],
        password=payload["password"],
        roles_id=STAFF_ROLE_ID,   # ép role staff
        created_at=now,
        updated_at=now,
    )
    return jsonify(response_schema.dump(staff)), 201


@bp.route("/<int:user_id>", methods=["PUT"])
def update_staff(user_id: int):
    """
    PUT /staffs/<id>
    Cập nhật hồ sơ staff cơ bản; không cho đổi role & (thường) không đổi password ở đây.
    """
    data = request.get_json() or {}
    try:
        payload = update_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    current = user_service.get_user(user_id)
    if not current or getattr(current, "roles_id", None) != STAFF_ROLE_ID:
        return jsonify({"message": "Staff not found"}), 404

    now = datetime.utcnow()
    staff = user_service.update_user(
        user_id=user_id,
        username=payload.get("username", current.username),
        email=payload.get("email", current.email),
        password=current.password,       # KHÔNG đổi password ở đây
        roles_id=STAFF_ROLE_ID,          # giữ đúng role staff
        created_at=current.created_at,   # giữ nguyên created_at
        updated_at=now,
    )
    return jsonify(response_schema.dump(staff)), 200


@bp.route("/<int:user_id>", methods=["DELETE"])
def delete_staff(user_id: int):
    """DELETE /staffs/<id>"""
    u = user_service.get_user(user_id)
    if not u or getattr(u, "roles_id", None) != STAFF_ROLE_ID:
        return jsonify({"message": "Staff not found"}), 404
    user_service.delete_user(user_id)
    return "", 204
