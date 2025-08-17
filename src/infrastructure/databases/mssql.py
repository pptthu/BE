from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus
import os

Base = declarative_base()

def _truthy(x: str | None) -> bool:
    return str(x).lower() in ("1", "true", "yes", "y")

def _build_uri() -> str:
    driver = os.getenv("MSSQL_DRIVER", "ODBC Driver 18 for SQL Server")
    host   = os.getenv("MSSQL_HOST", "127.0.0.1")
    port   = os.getenv("MSSQL_PORT", "1433")
    db     = os.getenv("MSSQL_DB", "BookSysDB")

    dburi = os.getenv("DATABASE_URI")
    if dburi:
        return dburi

    # Windows Auth (Trusted_Connection)
    if _truthy(os.getenv("MSSQL_TRUSTED")) or not os.getenv("MSSQL_USER"):
        return (
            f"mssql+pyodbc://@{host},{port}/{db}"
            f"?driver={quote_plus(driver)}"
            f"&Trusted_Connection=yes&TrustServerCertificate=yes"
        )

    # SQL Auth
    user = os.getenv("MSSQL_USER", "")
    pwd  = os.getenv("MSSQL_PASSWORD", "")
    return (
        f"mssql+pyodbc://{quote_plus(user)}:{quote_plus(pwd)}@{host},{port}/{db}"
        f"?driver={quote_plus(driver)}&TrustServerCertificate=yes"
    )

DATABASE_URI = _build_uri()
engine = create_engine(DATABASE_URI, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def get_session():
    return SessionLocal

def init_db():
    # Import models để đăng ký đầy đủ mapper/relationship
    import src.infrastructure.models  # noqa: F401
    Base.metadata.create_all(bind=engine)
