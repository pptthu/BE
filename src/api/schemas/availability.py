#khách tra slot trống POD
from marshmallow import Schema, fields

class PodAvailabilityRequestSchema(Schema):
    location_id = fields.Int(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)

class PodAvailabilityItemSchema(Schema):
    pod_id = fields.Int(required=True)
    name = fields.Str(required=False)
    price = fields.Float(required=False)

class PodAvailabilityResponseSchema(Schema):
    items = fields.List(fields.Nested(PodAvailabilityItemSchema), required=True)
