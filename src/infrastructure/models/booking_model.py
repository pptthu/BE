from src.infrastructure.databases.extensions import db

class Booking(db.Model):
    __tablename__ = "Bookings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
    pod_id  = db.Column(db.Integer, db.ForeignKey("PODs.id"), nullable=False)

    start_time = db.Column(db.DateTime, nullable=False)
    end_time   = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)

    status = db.Column(db.String(20), nullable=False, default="pending")
    payment_status = db.Column(db.String(20), nullable=False, default="unpaid")
    payment_confirmed_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, server_default=db.func.now(), onupdate=db.func.now()
    )

    user = db.relationship("User", backref="bookings")
    pod  = db.relationship("POD", backref="bookings")
