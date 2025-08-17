from functools import wraps
from typing import Tuple
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity

ROLE_WEIGHT = {"customer": 1, "staff": 2, "manager": 3, "admin": 4}

def role_required(*allowed: Tuple[str]):
    def wrapper(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            ident = get_jwt_identity() or {}
            role = claims.get("role") or ident.get("role")
            if role not in allowed:
                return jsonify({"message": "Forbidden", "required": allowed, "role": role}), 403
            return fn(*args, **kwargs)
        return inner
    return wrapper

def min_role(required: str):
    req_w = ROLE_WEIGHT.get(required, 0)
    def wrapper(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            ident = get_jwt_identity() or {}
            role = claims.get("role") or ident.get("role")
            if ROLE_WEIGHT.get(role, 0) < req_w:
                return jsonify({"message": "Forbidden", "min_required": required, "role": role}), 403
            return fn(*args, **kwargs)
        return inner
    return wrapper
