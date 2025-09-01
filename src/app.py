from flask import Flask
from src.api.routes import api
from src.common.error_handler import register_error_handlers
from src.infrastructure.databases.mssql import init_db, SessionLocal
from src.infrastructure.models.role_model import Role
from src.infrastructure.models.user_model import User
from src.common.security import hash_password
from src.common.constants import ROLES




def seed_data():
db = SessionLocal()
try:
# seed roles
role_names = [ROLES["ADMIN"], ROLES["MANAGER"], ROLES["STAFF"], ROLES["CUSTOMER"]]
roles = {}
for name in role_names:
r = db.query(Role).filter(Role.name == name).first()
if not r:
r = Role(name=name)
db.add(r); db.flush()
roles[name] = r
# seed users (idempotent by email)
def ensure(email, fullname, role_name):
u = db.query(User).filter(User.email == email).first()
if not u:
u = User(full_name=fullname, email=email,
password=hash_password("123456"), role_id=roles[role_name].id)
db.add(u)
ensure("admin@pod.local", "Admin", ROLES["ADMIN"])
ensure("manager@pod.local", "Manager", ROLES["MANAGER"])
ensure("staff@pod.local", "Staff", ROLES["STAFF"])
ensure("user@pod.local", "User", ROLES["CUSTOMER"])
db.commit()
finally:
SessionLocal.remove()


app = Flask(__name__)
init_db()
seed_data()


app.register_blueprint(api, url_prefix="/")
register_error_handlers(app)


@app.get("/")
def root():
return {"service": "POD Booking API", "status": "ok"}


if __name__ == "__main__":
app.run(host="0.0.0.0", port=6868, debug=True)