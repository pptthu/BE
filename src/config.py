import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET", "devsecret")

    DB_USER = os.getenv("DB_USER", "sa")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "Aa@123456")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "14333")
    DB_NAME = os.getenv("DB_NAME", "BookSysDB")
    ODBC_DRIVER = os.getenv("ODBC_DRIVER", "ODBC Driver 18 for SQL Server")

    SQLALCHEMY_DATABASE_URI = (
        "mssql+pyodbc://{user}:{pwd}@{host}:{port}/{db}"
        "?driver={driver}&TrustServerCertificate=yes"
    ).format(
        user=DB_USER,
        pwd=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        db=DB_NAME,
        driver=ODBC_DRIVER.replace(" ", "+")
    )
