from flask import Blueprint, request, g
from ...services.auth_service import AuthService
from ..schemas.auth import RegisterRequest, LoginRequest
from ..responses import ok, fail

bp = Blueprint("auth", __name__)

@bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    errors = RegisterRequest().validate(data)
    if errors:
        return fail(str(errors), 400)
    svc = AuthService(g.db)
    try:
        user = svc.register_customer(
            data["full_name"].strip(),
            data["email"].strip().lower(),
            data["password"]
        )
        return ok({"id": user.id, "email": user.email}, 201)
    except Exception as e:
        g.db.rollback()
        return fail(str(e), 400)

@bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    errors = LoginRequest().validate(data)
    if errors:
        return fail(str(errors), 400)
    svc = AuthService(g.db)
    token, user = svc.login(data["email"].strip().lower(), data["password"])
    if not token:
        return fail("Wrong credentials", 401)
    return ok({"token": token, "user": {"id": user.id, "email": user.email, "full_name": user.full_name, "role": user.role.name}})
