# src/api/controllers/customer_controller.py
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

bp = Blueprint("customers", __name__, url_prefix="/customers")

user_service = UserService(UserRepository())
create_schema = UserCreateRequestSchema()
update_schema = UserUpdateRequestSchema()
response_schema = UserResponseSchema()

# Đặt đúng ID role "customer" theo bảng roles
CUSTOMER_ROLE_ID = 3


@bp.route("/", methods=["GET"])
def list_customers():
    """GET /customers — liệt kê user có role = customer"""
    all_users = user_service.list_users()
    customers = [u for u in all_users if getattr(u, "roles_id", None) == CUSTOMER_ROLE_ID]
    return jsonify(response_schema.dump(customers, many=True)), 200


@bp.route("/<int:user_id>", methods=["GET"])
def get_customer(user_id: int):
    """GET /customers/<id>"""
    u = user_service.get_user(user_id)
    if not u or getattr(u, "roles_id", None) != CUSTOMER_ROLE_ID:
        return jsonify({"message": "Customer not found"}), 404
    return jsonify(response_schema.dump(u)), 200


@bp.route("/", methods=["POST"])
def create_customer():
    """
    POST /customers
    Body như UserCreateRequestSchema, nhưng roles_id sẽ bị ép về CUSTOMER_ROLE_ID
    """
    data = request.get_json() or {}
    try:
        payload = create_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    now = datetime.utcnow()
    user = user_service.create_user(
        username=payload["username"],
        email=payload["email"],
        password=payload["password"],
        roles_id=CUSTOMER_ROLE_ID,  # ép role
        created_at=now,
        updated_at=now,
    )
    return jsonify(response_schema.dump(user)), 201


@bp.route("/<int:user_id>", methods=["PUT"])
def update_customer(user_id: int):
    """
    PUT /customers/<id>
    Cập nhật hồ sơ cơ bản; không cho đổi role & password ở đây.
    """
    data = request.get_json() or {}
    try:
        payload = update_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    current = user_service.get_user(user_id)
    if not current or getattr(current, "roles_id", None) != CUSTOMER_ROLE_ID:
        return jsonify({"message": "Customer not found"}), 404

    now = datetime.utcnow()
    user = user_service.update_user(
        user_id=user_id,
        username=payload.get("username", current.username),
        email=payload.get("email", current.email),
        password=current.password,          # KHÔNG đổi password ở đây
        roles_id=CUSTOMER_ROLE_ID,          # giữ đúng role
        created_at=current.created_at,      # giữ nguyên created_at
        updated_at=now,
    )
    return jsonify(response_schema.dump(user)), 200


@bp.route("/<int:user_id>", methods=["DELETE"])
def delete_customer(user_id: int):
    """DELETE /customers/<id>"""
    u = user_service.get_user(user_id)
    if not u or getattr(u, "roles_id", None) != CUSTOMER_ROLE_ID:
        return jsonify({"message": "Customer not found"}), 404
    user_service.delete_user(user_id)
    return "", 204
