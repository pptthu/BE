# src/api/controllers/me_controller.py
from flask import Blueprint, request, jsonify
from datetime import datetime
from marshmallow import ValidationError

from services.user_service import UserService
from services.auth_service import AuthService
from infrastructure.repositories.user_repository import UserRepository
from api.schemas.me import (
    MeResponseSchema,
    MeUpdateSchema,
    MeChangePasswordSchema,
)

bp = Blueprint("me", __name__, url_prefix="/me")

# Dùng chung 1 in-memory repository cho cả 2 service để dữ liệu nhất quán
_user_repo = UserRepository()
user_service = UserService(_user_repo)
auth_service = AuthService(_user_repo)

resp_schema = MeResponseSchema()
update_schema = MeUpdateSchema()
change_pw_schema = MeChangePasswordSchema()


# Helper: lấy current user_id (demo: từ header hoặc query)
def _get_current_user_id():
    # Ưu tiên header X-User-Id, fallback sang query ?user_id=
    raw = request.headers.get("X-User-Id") or request.args.get("user_id")
    if not raw:
        return None
    try:
        return int(raw)
    except Exception:
        return None


@bp.route("/", methods=["GET"])
def get_me():
    """
    GET /me
    - Lấy thông tin user đang đăng nhập (demo: dựa vào X-User-Id hoặc ?user_id=)
    """
    user_id = _get_current_user_id()
    if not user_id:
        return jsonify({"error": "Thiếu user_id (header X-User-Id hoặc query ?user_id=)"}), 401

    user = auth_service.get_user(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(resp_schema.dump(user)), 200


@bp.route("/", methods=["PATCH"])
def update_me():
    """
    PATCH /me
    - Cập nhật profile cơ bản (username, email)
    - Không đổi password ở endpoint này
    Body theo MeUpdateSchema
    """
    user_id = _get_current_user_id()
    if not user_id:
        return jsonify({"error": "Thiếu user_id (header X-User-Id hoặc query ?user_id=)"}), 401

    current = auth_service.get_user(user_id)
    if not current:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json(silent=True) or {}
    try:
        payload = update_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    now = datetime.utcnow()
    # Giữ nguyên password hiện tại (update profile không đổi mật khẩu)
    updated = user_service.update_user(
        user_id=user_id,
        username=payload.get("username", current.username),
        email=payload.get("email", current.email),
        password=getattr(current, "password", ""),      # giữ nguyên
        roles_id=getattr(current, "roles_id", 0),       # không đổi role ở /me
        created_at=current.created_at,                  # giữ nguyên
        updated_at=now,
    )
    return jsonify(resp_schema.dump(updated)), 200


@bp.route("/change-password", methods=["POST"])
def change_password():
    """
    POST /me/change-password
    Body:
    {
      "old_password": "...",
      "new_password": "..."
    }
    """
    user_id = _get_current_user_id()
    if not user_id:
        return jsonify({"error": "Thiếu user_id (header X-User-Id hoặc query ?user_id=)"}), 401

    data = request.get_json(silent=True) or {}
    try:
        payload = change_pw_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    ok = auth_service.change_password(
        user_id=user_id,
        old_password=payload["old_password"],
        new_password=payload["new_password"],
    )
    if not ok:
        return jsonify({"error": "Sai mật khẩu cũ hoặc user không tồn tại"}), 400

    return jsonify({"message": "Đổi mật khẩu thành công"}), 200
