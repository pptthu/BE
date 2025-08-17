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

bp = Blueprint("users", __name__, url_prefix="/users")

# Khởi tạo service + repository (memory, chưa kết nối DB thật)
user_service = UserService(UserRepository())

create_schema = UserCreateRequestSchema()
update_schema = UserUpdateRequestSchema()
response_schema = UserResponseSchema()


@bp.route("/", methods=["GET"])
def list_users():
    """GET /users"""
    users = user_service.list_users()
    return jsonify(response_schema.dump(users, many=True)), 200


@bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    """GET /users/<id>"""
    user = user_service.get_user(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(response_schema.dump(user)), 200


@bp.route("/", methods=["POST"])
def create_user():
    """
    POST /users
    Body:
    {
      "username": "...",
      "email": "...",
      "password": "...",
      "roles_id": 2
    }
    """
    data = request.get_json() or {}
    try:
        payload = create_schema.load(data)  # validate + deserialize
    except ValidationError as err:
        return jsonify(err.messages), 400

    now = datetime.utcnow()
    user = user_service.create_user(
        username=payload["username"],
        email=payload["email"],
        password=payload["password"],
        roles_id=payload["roles_id"],
        created_at=now,
        updated_at=now,
    )
    return jsonify(response_schema.dump(user)), 201


@bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id: int):
    """
    PUT /users/<id>
    Body (partial theo schema update):
    {
      "username": "...",   // optional
      "email": "...",      // optional
      "roles_id": 2        // optional
      // password KHÔNG cập nhật ở endpoint này
    }
    """
    data = request.get_json() or {}
    try:
        payload = update_schema.load(data)  # validate + deserialize
    except ValidationError as err:
        return jsonify(err.messages), 400

    current = user_service.get_user(user_id)
    if not current:
        return jsonify({"message": "User not found"}), 404

    now = datetime.utcnow()
    user = user_service.update_user(
        user_id=user_id,
        username=payload.get("username", current.username),
        email=payload.get("email", current.email),
        password=current.password,  # không đổi password ở đây
        roles_id=payload.get("roles_id", current.roles_id),
        created_at=current.created_at,  # giữ nguyên
        updated_at=now,
    )
    return jsonify(response_schema.dump(user)), 200


@bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int):
    """DELETE /users/<id>"""
    user_service.delete_user(user_id)
    return "", 204
