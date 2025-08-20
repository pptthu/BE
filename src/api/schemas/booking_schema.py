from marshmallow import Schema, fields
from src.api.schemas.pod_schema import PODSchema
from src.api.schemas.user_schema import UserSchema
from src.api.schemas.service_schema import ServiceSchema

class BookingServiceItemSchema(Schema):
    service = fields.Nested(ServiceSchema)
    quantity = fields.Int()

class BookingSchema(Schema):
    id = fields.Int()
    user = fields.Nested(UserSchema)
    pod = fields.Nested(PODSchema)
    start_time = fields.DateTime()
    end_time = fields.DateTime()
    total_price = fields.Float()
    status = fields.Str()
    payment_status = fields.Str()
    payment_confirmed_at = fields.DateTime(allow_none=True)
    booking_services = fields.List(fields.Nested(BookingServiceItemSchema))
