mport logging
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from dotenv import load_dotenv

# Load .env file
load_dotenv(dotenv_path="src/.env")


def _as_bool(v, default=False):
    if v is None:
        return default
    return str(v).strip().lower() in ("1", "true", "yes", "y", "on")

DRIVER = getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
HOST = getenv("DB_HOST")
PORT = getenv("DB_PORT")
NAME = getenv("DB_NAME")
USER = getenv("DB_USER")
PWD = getenv("DB_PASSWORD")
ENCRYPT = _as_bool(getenv("DB_ENCRYPT"), True)
TRUST_CERT = _as_bool(getenv("DB_TRUST_SERVER_CERT"), True)  # DEV default True
TIMEOUT = int(getenv("DB_CONNECT_TIMEOUT", "5"))

def _odbc_connect():
    conn = (
        f"DRIVER={DRIVER};"
        f"SERVER={HOST},{PORT};"
        f"DATABASE={NAME};"
        f"UID={USER};PWD={PWD};"
        f"Encrypt={'yes' if ENCRYPT else 'no'};"
        f"TrustServerCertificate={'yes' if TRUST_CERT else 'no'};"
        f"Connection Timeout={TIMEOUT};"
    )
    return quote_plus(conn)

DB_URL = f"mssql+pyodbc:///?odbc_connect={_odbc_connect()}"
engine = create_engine(
    DB_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,  # tự phục hồi kết nối chết
)

# Kiểm tra kết nối ban đầu + log ngắn gọn
logger = logging.getLogger("mssql")
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        logger.info("MSSQL connected")
except Exception as exc:
    logger.exception("MSSQL connection failed: %s", exc)
    raise

SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

# Base cho ORM
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass
