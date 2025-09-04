from functools import wraps
from flask import request
from .responses import fail
from .requests import decode_jwt

def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return fail("Missing Bearer token, use: Authorization: Bearer <token>", 401)
        token = auth.split(" ", 1)[1]
        payload = decode_jwt(token)
        if not payload:
            return fail("Invalid or expired token", 401)
        request.user = payload
        return fn(*args, **kwargs)
    return wrapper

def roles_required(*roles):
    def deco(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = getattr(request, "user", None)
            if not user:
                return fail("Unauthorized", 401)
            if user.get("role") not in roles:
                return fail("Forbidden", 403)
            return fn(*args, **kwargs)
        return wrapper
    return deco
