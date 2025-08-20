import os
from urllib.parse import quote_plus

class Config:
    # Core
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_change_me")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET", "dev_jwt_change_me")
    DEBUG = os.environ.get("DEBUG", "1") in ["1", "true", "True"]
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:3000")

    # DB Dialect: postgres | mssql
    DB_DIALECT = os.environ.get("DB_DIALECT", "postgres")

    # SQL Server
    DB_USER = os.environ.get("DB_USER", "sa")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "Aa@123456")
    DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.environ.get("DB_PORT", "1433"))
    DB_NAME = os.environ.get("DB_NAME", "BookSysDB")

    # Postgres
    PG_USER = os.environ.get("PG_USER", "postgres")
    PG_PASSWORD = os.environ.get("PG_PASSWORD", "postgres")
    PG_HOST = os.environ.get("PG_HOST", "127.0.0.1")
    PG_PORT = int(os.environ.get("PG_PORT", "5432"))
    PG_DB = os.environ.get("PG_DB", "booksysdb")

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        if self.DB_DIALECT == "mssql":
            return (
                f"mssql+pymssql://{self.DB_USER}:{quote_plus(self.DB_PASSWORD)}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )
        # default: postgres
        return (
            f"postgresql+psycopg2://{self.PG_USER}:{quote_plus(self.PG_PASSWORD)}"
            f"@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"
        )
