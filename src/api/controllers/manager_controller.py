from flask import Blueprint
from src.api.responses import success_response

bp = Blueprint("manager", __name__, url_prefix="/manager")

@bp.get("/health")
def health():
    return success_response({"status": "ok"}, "Manager health")
