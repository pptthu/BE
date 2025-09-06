<<<<<<< HEAD
# dependency_container.py  (đặt ở PROJECT ROOT, cùng cấp với thư mục src)
from __future__ import annotations

import os
from contextlib import contextmanager

# Tải .env nếu có (không bắt buộc)
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

SessionLocal = None  # sẽ gán bên dưới


def _try_import_sessionlocal():
    """
    Cố gắng lấy SessionLocal định nghĩa sẵn trong dự án.
    Ưu tiên: src.infrastructure.databases.base/mssql/mysql
    """
    global SessionLocal

    # Khi chạy python -m src.app, 'src' là package hợp lệ
    paths = [
        "src.infrastructure.databases.base",
        "src.infrastructure.databases.mssql",
        "src.infrastructure.databases.mysql",
        "src.infrastructure.database",      # phòng khi dự án dùng tên khác
        "src.infrastructure.db",            # "
    ]
    for mod in paths:
        try:
            m = __import__(mod, fromlist=["SessionLocal"])
            if hasattr(m, "SessionLocal"):
                SessionLocal = getattr(m, "SessionLocal")
                return True
        except Exception:
            continue
    return False


def _build_sessionlocal_from_env():
    """
    Tự dựng engine/session cho SQLAlchemy từ biến môi trường.
    - Ưu tiên: DATABASE_URL (ví dụ: mssql+pyodbc://sa:pass@localhost:1433/DB?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes)
    - Hoặc:   MSSQL_DSN / MSSQL_ODBC_DSN (ODBC connection string thuần)
    - Hoặc:   DB_* (DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, DB_DRIVER, DB_DIALECT)
    """
    global SessionLocal
    from sqlalchemy import create_engine  # type: ignore
    from sqlalchemy.orm import sessionmaker  # type: ignore
    from urllib.parse import quote_plus

    url = os.getenv("DATABASE_URL")

    # DSN thuần ODBC (mạnh cho SQL Server)
    odbc_dsn = os.getenv("MSSQL_ODBC_DSN") or os.getenv("MSSQL_DSN")

    if odbc_dsn:
        # mssql+pyodbc:///?odbc_connect=<quoted_dsn>
        params = quote_plus(odbc_dsn)
        url = f"mssql+pyodbc:///?odbc_connect={params}"

    if not url:
        # Ghép từ DB_* (mặc định MSSQL)
        dialect = os.getenv("DB_DIALECT", "mssql+pyodbc")
        host = os.getenv("DB_HOST", "127.0.0.1")
        port = os.getenv("DB_PORT", "1433")
        name = os.getenv("DB_NAME", "PodBooking")
        user = os.getenv("DB_USER", "sa")
        password = os.getenv("DB_PASSWORD", "123456")
        driver = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")

        if dialect.startswith("mssql+pyodbc"):
            # Mẫu URL MSSQL + pyodbc
            url = (
                f"mssql+pyodbc://{quote_plus(user)}:{quote_plus(password)}"
                f"@{host}:{port}/{quote_plus(name)}"
                f"?driver={quote_plus(driver)}&TrustServerCertificate=yes"
            )
        else:
            # MySQL/Postgres... (tự chịu trách nhiệm về driver)
            url = f"{dialect}://{user}:{password}@{host}:{port}/{name}"

    # Cuối cùng vẫn không có => fallback SQLite (để không crash, nhưng bạn nên dùng MSSQL)
    if not url:
        url = "sqlite:///./app.db"

    # Tạo engine & SessionLocal
    connect_args = {}
    if url.startswith("mssql+pyodbc"):
        # Tuỳ chọn hữu ích cho pyodbc
        connect_args["timeout"] = int(os.getenv("DB_CONN_TIMEOUT", "30"))

    engine = create_engine(
        url,
        pool_pre_ping=True,
        future=True,  # SA 1.4/2.0 đều OK
        connect_args=connect_args,
    )
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db_session():
    """
    Trả về phiên làm việc SQLAlchemy mới.
    Ưu tiên dùng SessionLocal có sẵn trong dự án; nếu không có thì tự dựng từ ENV.
    """
    global SessionLocal
    if SessionLocal is None:
        if not _try_import_sessionlocal():
            _build_sessionlocal_from_env()
    if SessionLocal is None:
        raise RuntimeError(
            "Không tạo được SessionLocal. Kiểm tra lại DATABASE_URL hoặc MSSQL_DSN/DB_*."
        )
    return SessionLocal()  # type: ignore


@contextmanager
def session_scope():
    """Context manager: commit/rollback an toàn."""
    db = get_db_session()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        try:
            db.close()
        except Exception:
            pass
=======
class Container:
    pass

container = Container()
>>>>>>> origin/main
