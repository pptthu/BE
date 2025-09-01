import os
from dotenv import load_dotenv
load_dotenv()


JWT_SECRET = os.getenv("JWT_SECRET", "change_me")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "120"))
API_PORT = int(os.getenv("API_PORT", "8000"))
PAYMENT_QR_PATH = os.getenv("PAYMENT_QR_PATH", "./static/qr/qr.png")