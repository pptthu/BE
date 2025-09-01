import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from config import Config
from extensions import db, jwt

# Blueprints
from routes.auth import bp as auth_bp
from routes.users import bp as users_bp
from routes.pods import bp as pods_bp
from routes.bookings import bp as bookings_bp
from routes.staff import bp as staff_bp
from routes.manager import bp as manager_bp
from routes.admin import bp as admin_bp

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    # Đăng ký route
    app.register_blueprint(auth_bp, url_prefix="/")
    app.register_blueprint(users_bp, url_prefix="/")
    app.register_blueprint(pods_bp, url_prefix="/")
    app.register_blueprint(bookings_bp, url_prefix="/")
    app.register_blueprint(staff_bp, url_prefix="/")
    app.register_blueprint(manager_bp, url_prefix="/")
    app.register_blueprint(admin_bp, url_prefix="/")

    @app.get("/health")
    def health():
        return jsonify(ok=True)

    # Khởi tạo bảng (MVP)
    with app.app_context():
        from models import role, user, location, pod, booking  # noqa: F401
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
