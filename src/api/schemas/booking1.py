
from marshmallow import Schema, fields

class BookingRequestSchema(Schema):
    user_id = fields.Int(required=True)
    pod_id = fields.Int(required=True)
    start_time = fields.DateTime(required=True)  # ISO 8601
    end_time = fields.DateTime(required=True)    # ISO 8601
    status = fields.Str(required=True)           # ví dụ: PENDING/CONFIRMED/...

class BookingResponseSchema(Schema):
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    pod_id = fields.Int(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    status = fields.Str(required=True)
    total_price = fields.Float(required=True)   
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
