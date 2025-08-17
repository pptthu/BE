from flask import Blueprint
from src.api.responses import success_response

bp = Blueprint("admin", __name__, url_prefix="/admin")

@bp.get("/health")
def health():
    return success_response({"status": "ok"}, "Admin health")
