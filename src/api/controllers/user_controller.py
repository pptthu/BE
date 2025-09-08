from flask import Blueprint, request, g
from ..middleware import auth_required
from ...services.user_service import UserService
from ..responses import ok, fail

bp = Blueprint("user", __name__)

@bp.get("/me/profile")
@auth_required
def me_profile():
    svc = UserService(g.db)
    me = svc.get_me(request.user["id"])
    return ok(me)

@bp.put("/me/profile")
@auth_required
def update_profile():
    data = request.get_json(silent=True) or {}
    full_name = (data.get("full_name") or "").strip()
    svc = UserService(g.db)
    me = svc.update_me(request.user["id"], full_name=full_name)
    return ok(me)

@bp.put("/me/email")
@auth_required
def change_email():
    data = request.get_json(silent=True) or {}
    new_email = (data.get("email") or "").strip().lower()
    if not new_email:
        return fail("Email is required", 400)
    svc = UserService(g.db)
    try:
        me = svc.change_email(request.user["id"], new_email)
        return ok(me)
    except Exception as e:
        g.db.rollback()
        return fail(str(e), 400)
