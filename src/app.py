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
# ---------------------------------------------------------------------


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