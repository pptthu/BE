<<<<<<< HEAD
# src/api/controllers/bookings_controller.py
from __future__ import annotations

import os
import sys
from types import SimpleNamespace
from flask import Blueprint, request, jsonify, g
import jwt  # PyJWT

from ...services.booking_service import BookingService
from ...infrastructure.repositories.booking_repository import BookingRepository

# ---------------------------------------------------------------------
# Robust import get_db_session
# 1) Cố import từ ROOT: dependency_container.py
# 2) Nếu chưa được, thêm ROOT vào sys.path rồi import lại
# 3) Nếu vẫn chưa được, thử src/utils/dependency_container.py
# 4) Cuối cùng, tự build SessionLocal từ ENV (DATABASE_URL / MSSQL_DSN / DB_*)
# ---------------------------------------------------------------------
get_db_session = None  # type: ignore

try:
    from dependency_container import get_db_session as _get_db_session  # type: ignore
    get_db_session = _get_db_session
except Exception:
    # Thêm project root vào sys.path rồi thử lại
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    if ROOT_DIR not in sys.path:
        sys.path.insert(0, ROOT_DIR)
    try:
        from dependency_container import get_db_session as _get_db_session  # type: ignore
        get_db_session = _get_db_session
    except Exception:
        try:
            from ...utils.dependency_container import get_db_session as _get_db_session  # type: ignore
            get_db_session = _get_db_session
        except Exception:
            # Fallback cuối: tự tạo SessionLocal từ ENV
            from sqlalchemy import create_engine  # type: ignore
            from sqlalchemy.orm import sessionmaker  # type: ignore
            from urllib.parse import quote_plus

            def _build_engine_url() -> str:
                url = os.getenv("DATABASE_URL")
                odbc_dsn = os.getenv("MSSQL_ODBC_DSN") or os.getenv("MSSQL_DSN")
                if not url and odbc_dsn:
                    return "mssql+pyodbc:///?odbc_connect=" + quote_plus(odbc_dsn)

                if url:
                    return url

                dialect = os.getenv("DB_DIALECT", "sqlite")
                if dialect.startswith("sqlite"):
                    return "sqlite:///./app.db"

                host = os.getenv("DB_HOST", "127.0.0.1")
                port = os.getenv("DB_PORT", "1433")
                name = os.getenv("DB_NAME", "PodBooking")
                user = os.getenv("DB_USER", "sa")
                password = os.getenv("DB_PASSWORD", "123456")
                driver = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")

                if dialect.startswith("mssql+pyodbc"):
                    return (
                        f"mssql+pyodbc://{quote_plus(user)}:{quote_plus(password)}"
                        f"@{host}:{port}/{quote_plus(name)}"
                        f"?driver={quote_plus(driver)}&TrustServerCertificate=yes"
                    )
                return f"{dialect}://{user}:{password}@{host}:{port}/{name}"

            _engine = create_engine(_build_engine_url(), pool_pre_ping=True, future=True)
            _SessionLocal = sessionmaker(bind=_engine, autocommit=False, autoflush=False)

            def get_db_session():  # type: ignore
                return _SessionLocal()


# Lấy SECRET/ALGO cho JWT (ưu tiên utils.config.settings, sau đó ENV, cuối cùng mặc định)
try:
    from ...utils.config import settings  # type: ignore
    JWT_SECRET = getattr(settings, "JWT_SECRET", os.getenv("JWT_SECRET", "dev-secret"))
    JWT_ALGO = getattr(settings, "JWT_ALGO", os.getenv("JWT_ALGO", "HS256"))
except Exception:
    JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
    JWT_ALGO = os.getenv("JWT_ALGO", "HS256")

bp = Blueprint("bookings", __name__)


def _service() -> tuple[BookingService, object]:
    db = get_db_session()
    return BookingService(BookingRepository(db)), db


def _current_user_from_header():
    """
    Fallback: tự decode JWT từ Authorization header.
    Hỗ trợ claim: id/user_id/sub, role/role_name/scope, email, full_name/name.
    """
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    token = auth.split(" ", 1)[1].strip()
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO], options={"verify_aud": False})
    except Exception:
        return None

    uid = payload.get("id") or payload.get("user_id") or payload.get("sub")
    if uid is None:
        return None
    role = payload.get("role") or payload.get("role_name") or payload.get("scope")
    full_name = payload.get("full_name") or payload.get("name")
    email = payload.get("email")
    try:
        uid = int(uid)
    except Exception:
        pass
    return SimpleNamespace(id=uid, role=role, full_name=full_name, email=email)


# ---------------------------------------------------------------------
# POST /bookings  (Customer tạo booking)
# Body: { "pod_id": 1, "start_time": "2026-01-02T09:00:00", "end_time": "2026-01-02T11:00:00" }
# Header: Authorization: Bearer {{customerToken}}
# ---------------------------------------------------------------------
@bp.route("/bookings", methods=["POST"])
def create_booking():
    payload = request.get_json(silent=True) or {}
    current_user = getattr(g, "current_user", None) or getattr(g, "user", None) or _current_user_from_header()
    if current_user is None:
        return jsonify({"ok": False, "error": "Unauthorized: invalid or missing token"}), 401

    svc, db = _service()
    try:
        booking = svc.create_booking(current_user=current_user, data=payload)
        return (
            jsonify(
                {
                    "ok": True,
                    "data": {
                        "id": booking.id,
                        "pod_id": booking.pod_id,
                        "start_time": booking.start_time.isoformat(),
                        "end_time": booking.end_time.isoformat(),
                        "status": booking.status,
                    },
                }
            ),
            201,
        )
    except Exception as ex:
        return jsonify({"ok": False, "error": str(ex)}), 400
    finally:
        try:
            db.close()
        except Exception:
            pass


# ---------------------------------------------------------------------
# GET /bookings  (Customer – danh sách booking của chính mình)
# ---------------------------------------------------------------------
@bp.route("/bookings", methods=["GET"])
def my_bookings():
    current_user = getattr(g, "current_user", None) or getattr(g, "user", None) or _current_user_from_header()
    if current_user is None:
        return jsonify({"ok": False, "error": "Unauthorized: invalid or missing token"}), 401

    svc, db = _service()
    try:
        rows = svc.my_bookings(current_user=current_user)
        return jsonify(
            {
                "ok": True,
                "data": [
                    {
                        "id": r.id,
                        "pod_id": r.pod_id,
                        "start_time": r.start_time.isoformat(),
                        "end_time": r.end_time.isoformat(),
                        "status": r.status,
                    }
                    for r in rows
                ],
            }
        )
    except Exception as ex:
        return jsonify({"ok": False, "error": str(ex)}), 400
    finally:
        try:
            db.close()
        except Exception:
            pass


# ---------------------------------------------------------------------
# GET /bookings/<booking_id>  (chi tiết booking)
# ---------------------------------------------------------------------
@bp.route("/bookings/<int:booking_id>", methods=["GET"])
def get_booking(booking_id: int):
    current_user = getattr(g, "current_user", None) or getattr(g, "user", None) or _current_user_from_header()
    if current_user is None:
        return jsonify({"ok": False, "error": "Unauthorized: invalid or missing token"}), 401

    svc, db = _service()
    try:
        row = svc.repo.get_by_id(booking_id)
        if not row:
            return jsonify({"ok": False, "error": "Not found"}), 404
        return jsonify(
            {
                "ok": True,
                "data": {
                    "id": row.id,
                    "pod_id": row.pod_id,
                    "start_time": row.start_time.isoformat(),
                    "end_time": row.end_time.isoformat(),
                    "status": row.status,
                },
            }
        )
    except Exception as ex:
        return jsonify({"ok": False, "error": str(ex)}), 400
    finally:
        try:
            db.close()
        except Exception:
            pass


# ---------------------------------------------------------------------
# POST /bookings/<booking_id>/confirm-payment  (Customer xác nhận thanh toán)
# ---------------------------------------------------------------------
@bp.route("/bookings/<int:booking_id>/confirm-payment", methods=["POST"])
def confirm_payment(booking_id: int):
    current_user = getattr(g, "current_user", None) or getattr(g, "user", None) or _current_user_from_header()
    if current_user is None:
        return jsonify({"ok": False, "error": "Unauthorized: invalid or missing token"}), 401

    svc, db = _service()
    try:
        row = svc.confirm_payment(booking_id)
        if not row:
            return jsonify({"ok": False, "error": "Not found"}), 404
        return jsonify({"ok": True})
    except Exception as ex:
        return jsonify({"ok": False, "error": str(ex)}), 400
    finally:
        try:
            db.close()
        except Exception:
            pass
=======
from flask import Blueprint, request, g, current_app, send_file, url_for
from ..middleware import auth_required
from ...services.booking_service import BookingService
from ..responses import ok, fail
from ..schemas.booking import CreateBookingRequest
import os

bp = Blueprint("bookings", __name__)

@bp.post("/bookings")
@auth_required
def create_booking():
    data = request.get_json(silent=True) or {}
    errors = CreateBookingRequest().validate(data)
    if errors:
        return fail(str(errors), 400)
    svc = BookingService(g.db)
    try:
        booking = svc.create_booking(
            user_id=request.user["id"],
            pod_id=data["pod_id"],
            start_time=data["start_time"],
            end_time=data["end_time"],
        )
        return ok(booking, 201)
    except Exception as e:
        g.db.rollback()
        return fail(str(e), 400)

@bp.get("/bookings")
@auth_required
def list_my_bookings():
    svc = BookingService(g.db)
    items = svc.list_my_bookings(user_id=request.user["id"])
    return ok(items)

@bp.get("/bookings/<int:booking_id>")
@auth_required
def get_booking(booking_id: int):
    svc = BookingService(g.db)
    b = svc.get(booking_id, owner_id=request.user["id"])
    if not b:
        return fail("Not found", 404)
    return ok(b)

@bp.get("/bookings/<int:booking_id>/payment")
@auth_required
def get_booking_payment(booking_id: int):
    svc = BookingService(g.db)
    b = svc.get(booking_id, owner_id=request.user["id"])
    if not b:
        return fail("Not found", 404)
    b["qr_url"] = url_for("bookings.get_qr", _external=True)
    return ok(b)

@bp.post("/bookings/<int:booking_id>/confirm-payment")
@auth_required
def confirm_payment(booking_id: int):
    svc = BookingService(g.db)
    try:
        booking = svc.confirm_payment(user_id=request.user["id"], booking_id=booking_id)
        return ok(booking)
    except Exception as e:
        g.db.rollback()
        return fail(str(e), 400)

@bp.get("/payment/qr")
def get_qr():
    path = current_app.config.get("PAYMENT_QR_PATH", "./static/qr/qr.png")
    if not os.path.exists(path):
        return fail("QR image not found", 404)
    return send_file(path, mimetype="image/png")
>>>>>>> origin/main
