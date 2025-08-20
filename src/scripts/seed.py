from src.create_app import create_app
from src.infrastructure.databases.extensions import db
from src.infrastructure.models.role_model import Role
from src.infrastructure.models.user_model import User
from src.infrastructure.models.location_model import Location
from src.infrastructure.models.pod_model import POD

def main():
    app = create_app()
    with app.app_context():
        # 1) Roles
        for r in ["admin", "manager", "staff", "customer"]:
            if not Role.query.filter_by(name=r).first():
                db.session.add(Role(name=r))
        db.session.commit()

        # 2) Locations
        for name, addr in [("Campus A", "01 Main St"), ("Campus B", "02 Second St")]:
            if not Location.query.filter_by(name=name).first():
                db.session.add(Location(name=name, address=addr))
        db.session.commit()

        # 3) Users
        admin = Role.query.filter_by(name="admin").first()
        manager = Role.query.filter_by(name="manager").first()
        staff = Role.query.filter_by(name="staff").first()
        customer = Role.query.filter_by(name="customer").first()

        if not User.query.filter_by(email="admin@example.com").first():
            u = User(email="admin@example.com", full_name="Admin", role_id=admin.id)
            u.set_password("Aa@123456")
            db.session.add(u)

        if not User.query.filter_by(email="manager@example.com").first():
            u = User(email="manager@example.com", full_name="Manager", role_id=manager.id)
            u.set_password("Aa@123456")
            db.session.add(u)

        loc1 = Location.query.filter_by(name="Campus A").first()
        if not User.query.filter_by(email="staff@example.com").first():
            u = User(
                email="staff@example.com",
                full_name="Staff A",
                role_id=staff.id,
                location_id=loc1.id if loc1 else None,
            )
            u.set_password("Aa@123456")
            db.session.add(u)

        if not User.query.filter_by(email="customer@example.com").first():
            u = User(email="customer@example.com", full_name="Customer", role_id=customer.id)
            u.set_password("Aa@123456")
            db.session.add(u)

        db.session.commit()

        # 4) PODs
        if loc1 and not POD.query.filter_by(name="POD-A1", location_id=loc1.id).first():
            db.session.add(POD(name="POD-A1", price=30000, status="active", location_id=loc1.id))

        loc2 = Location.query.filter_by(name="Campus B").first()
        if loc2 and not POD.query.filter_by(name="POD-B1", location_id=loc2.id).first():
            db.session.add(POD(name="POD-B1", price=35000, status="active", location_id=loc2.id))

        db.session.commit()
        print("Seed done. Accounts: admin/manager/staff/customer @example.com / Aa@123456")

if __name__ == "__main__":
    main()
