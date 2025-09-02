
## Domain Layer

## Services Layer

## Infrastructure Layer

## Download source code (CMD)


 - Bước 1: Tạo môi trường ảo co Python (phiên bản 3.x)
     ## Windows:
     		py -m venv .venv
     ## Unix/MacOS:
     		python3 -m venv .venv
   - Bước 2: Kích hoạt môi trường:
     ## Windows:
     		.venv\Scripts\activate.ps1
     ### Nếu xảy ra lỗi active .venv trên winos run powshell -->Administrator
         Set-ExecutionPolicy RemoteSigned -Force
     ## Unix/MacOS:
     		source .venv/bin/activate
     
   - Bước 3: Cài đặt các thư viện cần thiết
     ## Install:
     		pip install -r requirements.txt
   - Bước 4: Chạy mã xử lý dữ liệu
     ## Run:
    		python app.py


     Truy câp http://localhost:6868/docs



## Create file .env 
    
ODBC_DRIVER=ODBC Driver 18 for SQL Server
ENCRYPT=yes
TRUST_SERVER_CERTIFICATE=yes
DB_HOST=127.0.0.1
DB_PORT=1433         # đổi nếu instance nghe cổng khác
DB_NAME=BookSysDB
DB_USER=sa
DB_PASSWORD=Aa@123456


JWT_SECRET=super_secret_change_me
JWT_EXPIRE_MINUTES=120
API_PORT=8000

PAYMENT_QR_PATH=/static/qr/qr.png


