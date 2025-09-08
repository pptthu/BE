import datetime as dt
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from ..config import load_config
_cfg = load_config()

def hash_password(pw: str) -> str: return generate_password_hash(pw)
def verify_password(pw: str, hashed: str) -> bool: return check_password_hash(hashed, pw)

def create_jwt(claims: dict) -> str:
    payload = claims.copy()
    payload["exp"] = dt.datetime.utcnow() + dt.timedelta(minutes=int(_cfg["JWT_EXPIRE_MINUTES"]))
    return jwt.encode(payload, _cfg["SECRET_KEY"], algorithm="HS256")

def decode_jwt(token: str) -> dict | None:
    try:
        return jwt.decode(token, _cfg["SECRET_KEY"], algorithms=["HS256"])
    except Exception:
        return None
