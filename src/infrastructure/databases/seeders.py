from src.infrastructure.models.role_model import RoleModel
from src.infrastructure.models.user_model import UserModel
from werkzeug.security import generate_password_hash

def seed_roles(session):
    roles = ["admin", "manager", "staff", "customer"]
    for r in roles:
        if not session.query(RoleModel).filter_by(name=r).first():
            session.add(RoleModel(name=r))
    session.commit()

def seed_admin(session):
    admin_email = "admin@example.com"
    admin = session.query(UserModel).filter_by(email=admin_email).first()
    if not admin:
        admin_role = session.query(RoleModel).filter_by(name="admin").first()
        if not admin_role:
            raise RuntimeError("Admin role not found, run seed_roles first.")
        admin = UserModel(
            full_name="System Administrator",
            email=admin_email,
            password=generate_password_hash("admin123"),  # mật khẩu mặc định
            role_id=admin_role.id
        )
        session.add(admin)
        session.commit()
        print("✅ Admin user created: admin@example.com / admin123")
    else:
        print("ℹ️ Admin user already exists.")
