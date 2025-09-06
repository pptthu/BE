<<<<<<< HEAD
import os
import urllib.parse
from dotenv import load_dotenv

def _to_bool(v: str | None, default: bool = False) -> bool:
    if v is None:
        return default
    return str(v).strip().lower() in ("1", "true", "yes", "on")

def load_config() -> dict:
    load_dotenv()
    return {
        "FLASK_ENV": os.getenv("FLASK_ENV", "development"),
        "SECRET_KEY": os.getenv("SECRET_KEY", "dev_secret"),

        "DB_USER": os.getenv("DB_USER", "sa"),
        "DB_PASSWORD": os.getenv("DB_PASSWORD", "Aa@123456"),
        "DB_HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "DB_PORT": int(os.getenv("DB_PORT", "14333")),
        "DB_NAME": os.getenv("DB_NAME", "BookSysDB"),

        "PAYMENT_QR_PATH": os.getenv("PAYMENT_QR_PATH", "./static/qr/qr.png"),
        "JWT_EXPIRE_MINUTES": int(os.getenv("JWT_EXPIRE_MINUTES", "120")),
        "FIRST_USER_ADMIN": _to_bool(os.getenv("FIRST_USER_ADMIN"), True),
    }

class Config:
    load_dotenv()
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
    DB_USER = os.getenv("DB_USER", "sa")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "Aa@123456")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "14333"))
    DB_NAME = os.getenv("DB_NAME", "BookSysDB")

    _odbc = urllib.parse.quote_plus(
        "DRIVER=ODBC Driver 18 for SQL Server;"
        f"SERVER={DB_HOST},{DB_PORT};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};PWD={DB_PASSWORD};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )
    DATABASE_URI = os.getenv("DATABASE_URI") or f"mssql+pyodbc:///?odbc_connect={_odbc}"
=======
import os
import urllib.parse
from dotenv import load_dotenv

def _to_bool(v: str | None, default: bool = False) -> bool:
    if v is None:
        return default
    return str(v).strip().lower() in ("1", "true", "yes", "on")

def load_config() -> dict:
    load_dotenv()
    return {
        "FLASK_ENV": os.getenv("FLASK_ENV", "development"),
        "SECRET_KEY": os.getenv("SECRET_KEY", "dev_secret"),

        "DB_USER": os.getenv("DB_USER", "sa"),
        "DB_PASSWORD": os.getenv("DB_PASSWORD", "Aa@123456"),
        "DB_HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "DB_PORT": int(os.getenv("DB_PORT", "14333")),
        "DB_NAME": os.getenv("DB_NAME", "BookSysDB"),

        "PAYMENT_QR_PATH": os.getenv("PAYMENT_QR_PATH", "./static/qr/qr.png"),
        "JWT_EXPIRE_MINUTES": int(os.getenv("JWT_EXPIRE_MINUTES", "120")),
        "FIRST_USER_ADMIN": _to_bool(os.getenv("FIRST_USER_ADMIN"), True),
    }

class Config:
    load_dotenv()
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
    DB_USER = os.getenv("DB_USER", "sa")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "Aa@123456")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "14333"))
    DB_NAME = os.getenv("DB_NAME", "BookSysDB")

    _odbc = urllib.parse.quote_plus(
        "DRIVER=ODBC Driver 18 for SQL Server;"
        f"SERVER={DB_HOST},{DB_PORT};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};PWD={DB_PASSWORD};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )
    DATABASE_URI = os.getenv("DATABASE_URI") or f"mssql+pyodbc:///?odbc_connect={_odbc}"
>>>>>>> origin/main
