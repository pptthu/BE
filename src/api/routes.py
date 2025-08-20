from flask import Flask
from .controllers.auth_controller import bp as auth_bp
from .controllers.users_controller import bp as user_bp
from .controllers.locations_controller import bp as location_bp
from .controllers.pods_controller import bp as pod_bp
from .controllers.bookings_controller import bp as booking_bp  # singular
from .controllers.staff_controller import bp as staff_bp
from .controllers.manager_controller import bp as manager_bp
from .controllers.admin_controller import bp as admin_bp
# Nếu không có todo_controller, đừng import nó.

def register_routes(app: Flask):
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(location_bp)
    app.register_blueprint(pod_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(manager_bp)
    app.register_blueprint(admin_bp)
