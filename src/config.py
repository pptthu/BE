import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "a_default_secret_key")
    DEBUG = os.getenv("DEBUG", "False").lower() in ["true", "1", "yes"]
    TESTING = os.getenv("TESTING", "False").lower() in ["true", "1", "yes"]

    # MSSQL (pyodbc + ODBC Driver 18)
    DB_USER = os.getenv("DB_USER", "sa")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "Aa@123456")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "1433"))
    DB_NAME = os.getenv("DB_NAME", "BookSysDB")
    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        "?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=no"
    )

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-jwt")

    # Flasgger
    SWAGGER_CONFIG = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec_1",
                "route": "/apispec_1.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
    }
    SWAGGER_TEMPLATE = {
        "swagger": "2.0",
        "info": {"title": "POD Booking System API", "version": "1.0.0"},
        "basePath": "/",
    }
