from marshmallow import Schema, fields, validate

class CreateBookingRequest(Schema):
    pod_id = fields.Integer(required=True)
    start_time = fields.String(required=True, validate=validate.Length(min=10))  # ISO 8601
    end_time = fields.String(required=True, validate=validate.Length(min=10))
