from src.infrastructure.databases.extensions import db

class BookingService(db.Model):
    __tablename__ = "Booking_Services"

    booking_id = db.Column(db.Integer, db.ForeignKey("Bookings.id"), primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey("Services.id"), primary_key=True)
    quantity   = db.Column(db.Integer, nullable=False, default=1)

    booking = db.relationship("Booking", backref="booking_services")
    service = db.relationship("Service", lazy="joined")
