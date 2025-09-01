from marshmallow import Schema, fields,validate
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
# Dùng cho trả danh sách / chi tiết booking
class BookingResponseSchema(Schema):
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    pod_id = fields.Int(required=True)

    # Trả ISO datetime cho client
    start_time = fields.DateTime(required=True)
    end_time   = fields.DateTime(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)

  
    status = fields.Str(required=True, validate=validate.OneOf([
       "confirmed", "checked_in", "checked_out"
    ]))



    # Tuỳ DB có hay không các trường dưới:
    # payment_status = fields.Str(allow_none=True)
    # check_in_at    = fields.DateTime(allow_none=True)
    # check_out_at   = fields.DateTime(allow_none=True)
    # checked_in_by  = fields.Int(allow_none=True)
    # checked_out_by = fields.Int(allow_none=True)


# (tuỳ chọn) Dùng khi tạo booking (nếu có endpoint create)
class BookingCreateRequestSchema(Schema):
    pod_id = fields.Int(required=True)
    start_time = fields.DateTime(required=True)  
    end_time   = fields.DateTime(required=True)
