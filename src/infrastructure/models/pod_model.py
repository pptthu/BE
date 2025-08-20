from src.infrastructure.databases.extensions import db

class POD(db.Model):
    __tablename__ = "PODs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="active")
    location_id = db.Column(db.Integer, db.ForeignKey("Locations.id"), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, server_default=db.func.now(), onupdate=db.func.now()
    )

    location = db.relationship("Location", backref="pods")
