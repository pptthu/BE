import jwt
import datetime
from flask import current_app, request
from functools import wraps

def generate_jwt(payload: dict, expires_in: int = 3600):
    """Tạo JWT token"""
    payload_copy = payload.copy()
    payload_copy["exp"] = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    return jwt.encode(payload_copy, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")

def decode_jwt(token: str):
    """Giải mã JWT token"""
    try:
        return jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def auth_required(roles=None):
    """
    Decorator: Yêu cầu login, optional kiểm tra role.
    Example:
        @auth_required(roles=["admin"])
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            token = None
            if "Authorization" in request.headers:
                parts = request.headers["Authorization"].split(" ")
                if len(parts) == 2 and parts[0] == "Bearer":
                    token = parts[1]

            if not token:
                return {"message": "Missing Authorization Header"}, 401

            data = decode_jwt(token)
            if not data:
                return {"message": "Invalid or expired token"}, 401

            # Kiểm tra role nếu có
            if roles and data.get("role") not in roles:
                return {"message": "Forbidden"}, 403

            # inject user info vào request
            request.user = data
            return fn(*args, **kwargs)
        return decorator
    return wrapper
