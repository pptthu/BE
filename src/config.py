import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    DB_USER = os.getenv("DB_USER", "sa")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "Aa@123456")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "14333"))
    DB_NAME = os.getenv("DB_NAME", "BookSysDB")

    JWT_SECRET = os.getenv("JWT_SECRET", "change_me")
    JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "120"))
    PAYMENT_QR_PATH = os.getenv("PAYMENT_QR_PATH", "./static/qr/qr.png")
    API_PORT = int(os.getenv("API_PORT", "8000"))

    @property
    def SQLALCHEMY_URL(self):
        return (f"mssql+pyodbc://{self.DB_USER}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
                f"?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes")

settings = Settings()
