from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def roles_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt() or {}
            if claims.get("role") not in roles:
                return jsonify({"error": "forbidden", "message": "Insufficient role"}), 403
            return fn(*args, **kwargs)
        return decorated
    return wrapper
