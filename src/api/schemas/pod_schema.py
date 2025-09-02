from marshmallow import Schema, fields

class PodRequestSchema(Schema):
    code = fields.Str(required=True)
    name = fields.Str(required=True)
    status = fields.Str(required=False)
    location_id = fields.Int(required=True)

class PodResponseSchema(Schema):
    id = fields.Int(required=True)
    code = fields.Str(required=True)
    name = fields.Str(required=True)
    status = fields.Str(required=True)
    location_id = fields.Int(required=True)
    created_at = fields.Raw()
    updated_at = fields.Raw()