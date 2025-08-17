from marshmallow import Schema, fields

class BookingSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    pod_id = fields.Int()
    start_time = fields.DateTime()
    end_time = fields.DateTime()
    total_price = fields.Decimal(as_string=True)  # DECIMAL(10,2)
    status = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
