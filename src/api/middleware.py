from functools import wraps
from flask import request, jsonify
import jwt
from src.config import JWT_SECRET

def require_auth(roles: list[str] | None = None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization", "")
            if not auth.startswith("Bearer "):
                return jsonify({"error": "Unauthorized"}), 401
            token = auth.split(" ", 1)[1]
            try:
                data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            except Exception:
                return jsonify({"error": "Invalid token"}), 401
            if roles and data.get("role") not in roles:
                return jsonify({"error": "Forbidden"}), 403
            request.user = data
            return fn(*args, **kwargs)
        return wrapper
    return decorator