from marshmallow import Schema, fields

class BookingResponseSchema(Schema):
    id          = fields.Int(required=True)
    user_id     = fields.Int(required=True)
    pod_id      = fields.Int(required=True)

    # FE hiển thị họ tên
    customer_name = fields.Method("get_customer_name")

    start_time  = fields.DateTime(required=True)
    end_time    = fields.DateTime(required=True)
    status      = fields.Str(required=True)
    total_price = fields.Decimal(as_string=True, allow_none=True)

    created_at  = fields.DateTime(allow_none=True)
    updated_at  = fields.DateTime(allow_none=True)

    def get_customer_name(self, obj):
        # an toàn khi không eagerload
        return getattr(getattr(obj, "user", None), "username", None)


class BookingRequestSchema(Schema):
    user_id    = fields.Int(required=True)
    pod_id     = fields.Int(required=True)
    start_time = fields.DateTime(required=True)
    end_time   = fields.DateTime(required=True)
    status     = fields.Str(required=True)  # PENDING/CONFIRMED/...
