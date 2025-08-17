# src/api/controllers/auth_controller.py
from datetime import timedelta
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

from src.infrastructure.databases import get_session
from src.services.user_service import UserService

from src.infrastructure.models.user_model import UserModel
from src.api.responses import success_response, error_response

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.post("/login")
def login():
    """
    Đăng nhập, trả về access_token (JWT) + thông tin role.
    Body:
    {
      "email": "customer@example.com",
      "password": "Aa@123456"
    }
    """
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return error_response("email & password are required", 400)

    session = get_session()()
    user = UserService.get_by_email(session, email)
    if not user or not UserService.verify_password(user, password):
        return error_response("Invalid email or password", 401)

    # Identity + Claims chứa role/email/name để middleware phân quyền sử dụng
    identity = {"user_id": user.id, "role": user.role.name}
    claims = {"role": user.role.name, "email": user.email, "name": user.full_name}

    access_token = create_access_token(
        identity=identity,
        additional_claims=claims,
        expires_delta=timedelta(hours=12),
    )

    return success_response({
        "access_token": access_token,
        "user_id": user.id,
        "role": user.role.name
    })


@bp.get("/me")
@jwt_required()
def me():
    """
    Trả về thông tin người dùng hiện tại (dựa trên JWT).
    """
    ident = get_jwt_identity() or {}
    claims = get_jwt() or {}
    session = get_session()()

    user = session.get(UserModel, ident.get("user_id"))
    if not user:
        return error_response("User not found", 404)

    return success_response({
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": claims.get("role") or ident.get("role"),
    })
