from .controllers.auth_controller import bp as auth_bp
from .controllers.user_controller import bp as user_bp
from .controllers.pods_controller import bp as pods_bp
from .controllers.bookings_controller import bp as bookings_bp
from .controllers.staff_controller import bp as staff_bp
from .controllers.manager_controller import bp as manager_bp
from .controllers.admin_controller import bp as admin_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/")
    app.register_blueprint(user_bp, url_prefix="/")
    app.register_blueprint(pods_bp, url_prefix="/")
    app.register_blueprint(bookings_bp, url_prefix="/")
    app.register_blueprint(staff_bp, url_prefix="/")
    app.register_blueprint(manager_bp, url_prefix="/")
    app.register_blueprint(admin_bp, url_prefix="/")
