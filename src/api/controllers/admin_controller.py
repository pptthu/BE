from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.infrastructure.databases import get_session
from src.infrastructure.models.user_model import UserModel
from src.api.schemas.user import UserSchema
from src.api.schemas.admin import UpdateRoleSchema
from src.services.user_service import UserService

bp = Blueprint("admin", __name__, url_prefix="/admin")

user_schema = UserSchema()
update_role_schema = UpdateRoleSchema()

def is_admin(session, ident):
    user = session.get(UserModel, ident.get("user_id"))
    return user and user.role and user.role.name == "admin"

@bp.get("/users")
@jwt_required()
def list_users():
    ident = get_jwt_identity()
    session = get_session()()
    if not is_admin(session, ident):
        return jsonify({"error": "Forbidden"}), 403
    
    users = UserService.list_all(session)
    return jsonify(user_schema.dump(users, many=True))

@bp.patch("/users/<int:user_id>/role")
@jwt_required()
def update_user_role(user_id):
    ident = get_jwt_identity()
    session = get_session()()
    if not is_admin(session, ident):
        return jsonify({"error": "Forbidden"}), 403

    data = update_role_schema.load(request.json)
    try:
        user = UserService.assign_role(session, user_id, data["role_name"])
        return jsonify(user_schema.dump(user))
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.delete("/users/<int:user_id>")
@jwt_required()
def delete_user(user_id):
    ident = get_jwt_identity()
    session = get_session()()
    if not is_admin(session, ident):
        return jsonify({"error": "Forbidden"}), 403

    try:
        UserService.delete_user(session, user_id)
        return jsonify({"message": "User deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
