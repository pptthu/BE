from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session

try:
    from ...config import Config
except Exception:
    Config = None

try:
    from .base import Base
except Exception:
    from ..models.base import Base

if Config and getattr(Config, "DATABASE_URI", None):
    DATABASE_URI = Config.DATABASE_URI
else:
    from ...config import load_config
    import urllib.parse
    _cfg = load_config()
    server = f"{_cfg['DB_HOST']},{_cfg['DB_PORT']}"
    odbc = (
        "DRIVER=ODBC Driver 18 for SQL Server;"
        f"SERVER={server};"
        f"DATABASE={_cfg['DB_NAME']};"
        f"UID={_cfg['DB_USER']};PWD={_cfg['DB_PASSWORD']};"
        "Encrypt=yes;TrustServerCertificate=yes;"
    )
    params = urllib.parse.quote_plus(odbc)
    DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"

engine = create_engine(DATABASE_URI, pool_pre_ping=True, fast_executemany=True)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def get_session():
    return SessionLocal()

def init_mssql(app=None):
    Base.metadata.create_all(bind=engine)
    return engine

@event.listens_for(engine, "connect")
def _on_connect(dbapi_connection, connection_record):
    try:
        cur = dbapi_connection.cursor()
        cur.execute("SET DATEFIRST 1;")
        cur.close()
    except Exception:
        pass
