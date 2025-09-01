<<<<<<< HEAD
from flask import Flask, jsonify
from api.swagger import spec
from api.controllers.todo_controller import bp as todo_bp
from api.middleware import middleware
from api.responses import success_response
from infrastructure.databases import init_db
from config import Config
from flasgger import Swagger
from config import SwaggerConfig
from flask_swagger_ui import get_swaggerui_blueprint


def create_app():
    app = Flask(__name__)
    Swagger(app)
    # Đăng ký blueprint trước
    app.register_blueprint(todo_bp)

     # Thêm Swagger UI blueprint
    SWAGGER_URL = '/docs'
    API_URL = '/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Todo API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    try:
        init_db(app)
    except Exception as e:
        print(f"Error initializing database: {e}")

    # Register middleware
    middleware(app)

    # Register routes
    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            # Thêm các endpoint khác nếu cần
            if rule.endpoint.startswith(('todo.', 'course.', 'user.')):
                view_func = app.view_functions[rule.endpoint]
                print(f"Adding path: {rule.rule} -> {view_func}")
                spec.path(view=view_func)

    @app.route("/swagger.json")
    def swagger_json():
        return jsonify(spec.to_dict())

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=6868, debug=True)
=======
from flask import Flask
from src.infrastructure.databases.db import init_db, SessionLocal
from src.error_handler import errors
from src.api.controllers.auth_controller import bp as auth_bp
from src.api.controllers.pods_controller import bp as pods_bp
from src.api.controllers.bookings_controller import bp as bookings_bp
from src.api.controllers.manager_controller import bp as manager_bp
from src.api.controllers.admin_controller import bp as admin_bp
from src.api.controllers.staff_controller import bp as staff_bp
from src.infrastructure.models.role import Role
from src.infrastructure.models.location import Location
from src.infrastructure.models.pod import POD
from src.domain.constants import ROLES
from src.config import API_PORT


app = Flask(__name__)


# Initialize DB (tables)
init_db()


# --- Bootstrap minimal data (idempotent, not a separate seed file) ---
def _bootstrap_minimal_data():
db = SessionLocal()
try:
# Roles
existing = {r.name for r in db.query(Role).all()}
for name in ROLES.values():
if name not in existing:
db.add(Role(name=name))
db.flush()


# 1 default Location
if db.query(Location).count() == 0:
loc = Location(name="Cơ sở 1", address="Quận 1, TP.HCM")
db.add(loc)
db.flush()
loc_id = loc.id
else:
loc_id = db.query(Location.id).first()[0]


# 5 PODs
existing_pods = {p.name for p in db.query(POD).all()}
defaults = [
("POD-101", 50000), ("POD-102", 50000), ("POD-103", 50000),
("POD-104", 60000), ("POD-105", 60000),
]
for name, price in defaults:
if name not in existing_pods:
db.add(POD(name=name, price=price, status="AVAILABLE", location_id=loc_id))
db.commit()
finally:
SessionLocal.remove()


_bootstrap_minimal_data()



# Register blueprints
app.register_blueprint(errors)
app.register_blueprint(auth_bp)
app.register_blueprint(pods_bp)
app.register_blueprint(bookings_bp)
app.register_blueprint(manager_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(staff_bp)


if __name__ == "__main__":
app.run(host="0.0.0.0", port=API_PORT, debug=True)
>>>>>>> 46e9165 (gửi file app.py)
