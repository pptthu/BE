from flask import Blueprint, request, g
from ..middleware import auth_required, roles_required
from ...services.manager_service import ManagerService
from ..responses import ok
from ...services.auth_service import AuthService

bp = Blueprint("admin", __name__)

@bp.get("/admin/users")
@auth_required
@roles_required("ADMIN")
def list_users():
    svc = ManagerService(g.db)
    return ok(svc.list_users())

@bp.post("/admin/users")
@auth_required
@roles_required("ADMIN")
def create_user():
    data = request.get_json(silent=True) or {}
    auth = AuthService(g.db)
    u = auth.register_customer(
        full_name=data.get("full_name"),
        email=(data.get("email") or "").strip().lower(),
        password=data.get("password") or "123456"
    )
    role = (data.get("role") or "").strip().upper()
    if role and role != "CUSTOMER":
        ManagerService(g.db).admin_update_user(u.id, role_name=role)
    return ok({"id": u.id, "email": u.email}, 201)

@bp.put("/admin/users/<int:user_id>")
@auth_required
@roles_required("ADMIN")
def update_user(user_id: int):
    data = request.get_json(silent=True) or {}
    svc = ManagerService(g.db)
    u = svc.admin_update_user(user_id, full_name=data.get("full_name"), role_name=data.get("role"))
    return ok(u)

@bp.delete("/admin/users/<int:user_id>")
@auth_required
@roles_required("ADMIN")
def delete_user(user_id: int):
    svc = ManagerService(g.db)
    svc.admin_delete_user(user_id)
    return ok(True)