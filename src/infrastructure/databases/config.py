import os
from dotenv import load_dotenv
load_dotenv()

class DBSettings:
    DB_USER = os.getenv("DB_USER", "sa")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "Aa@123456")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "14333"))
    DB_NAME = os.getenv("DB_NAME", "BookSysDB")

    @property
    def SQLALCHEMY_URL(self):
        return (f"mssql+pyodbc://{self.DB_USER}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
                f"?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes")

db_settings = DBSettings()