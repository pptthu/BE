from flask import Flask
from dotenv import load_dotenv
from src.config import Config
from src.app_logging import setup_logging
from src.cors import init_cors
from src.infrastructure.databases.extensions import db, jwt
from src.api.controllers.auth_controller import bp as auth_bp
from src.api.controllers.users_controller import bp as users_bp
from src.api.controllers.pods_controller import bp as pods_bp
from src.api.controllers.bookings_controller import bp as bookings_bp
from src.api.controllers.staff_controller import bp as staff_bp
from src.api.controllers.manager_controller import bp as manager_bp
from src.api.controllers.admin_controller import bp as admin_bp
from src.error_handler import register_error_handlers

def create_app():
    load_dotenv()
    setup_logging()
    app = Flask(__name__)

    cfg = Config()
    app.config.from_object(cfg)
    app.config["SQLALCHEMY_DATABASE_URI"] = cfg.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = cfg.JWT_SECRET_KEY

    db.init_app(app)
    jwt.init_app(app)
    init_cors(app)
    register_error_handlers(app)

    with app.app_context():
        # Import models để create_all (được cung cấp ở Phần 2)
        from src.infrastructure.models.role_model import Role
        from src.infrastructure.models.user_model import User
        from src.infrastructure.models.location_model import Location
        from src.infrastructure.models.pod_model import POD
        from src.infrastructure.models.service_model import Service
        from src.infrastructure.models.booking_model import Booking
        from src.infrastructure.models.booking_service_model import BookingService
        db.create_all()

    # Đăng ký router (controllers sẽ có ở Phần 5)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(pods_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(manager_bp)
    app.register_blueprint(admin_bp)

    return app

