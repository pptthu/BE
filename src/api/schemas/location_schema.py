from marshmallow import Schema, fields

class LocationRequestSchema(Schema):
    name = fields.Str(required=True)
    address = fields.Str(required=False)
    description = fields.Str(required=False)

class LocationResponseSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    address = fields.Str()
    description = fields.Str()
    created_at = fields.Raw()
    updated_at = fields.Raw()
