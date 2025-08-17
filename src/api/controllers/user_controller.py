from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.infrastructure.databases import get_session
from src.infrastructure.models.user_model import UserModel
from src.api.schemas.user import UserSchema
from src.api.responses import success_response
from src.services.user_service import UserService

bp = Blueprint("users", __name__, url_prefix="/users")
user_schema = UserSchema()

@bp.get("/me/profile")
@jwt_required()
def me():
    ident = get_jwt_identity() or {}
    session = get_session()()
    user = session.get(UserModel, ident.get("user_id"))
    data = user_schema.dump(user)
    data["role"] = user.role.name if user and user.role else None
    return success_response(data)
