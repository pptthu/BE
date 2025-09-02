import os
from dotenv import load_dotenv
from zoneinfo import ZoneInfo
load_dotenv()


JWT_SECRET = os.getenv("JWT_SECRET", "change_me")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "120"))
API_PORT = int(os.getenv("API_PORT", "8000"))
PAYMENT_QR_PATH = os.getenv("PAYMENT_QR_PATH", "/static/qr/qr.png")


# Timezone Việt Nam
VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")


# DB settings (SQL Server ODBC 18)
DB_USER = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Aa@123456")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "14333")
DB_NAME = os.getenv("DB_NAME", "BookSysDB")
ODBC_DRIVER = os.getenv("ODBC_DRIVER", "ODBC Driver 18 for SQL Server")
ENCRYPT = os.getenv("ENCRYPT", "yes")
TRUST_SERVER_CERTIFICATE = os.getenv("TRUST_SERVER_CERTIFICATE", "yes")