from src.infrastructure.databases.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey("Roles.id"), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, server_default=db.true())
    location_id = db.Column(db.Integer, db.ForeignKey("Locations.id"), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, server_default=db.func.now(), onupdate=db.func.now()
    )

    role = db.relationship("Role", backref="users")
    location = db.relationship(
        "Location", backref="staff", lazy="joined", foreign_keys=[location_id]
    )

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
