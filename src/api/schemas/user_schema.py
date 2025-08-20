from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int()
    full_name = fields.Str()
    email = fields.Str()
    role_id = fields.Int()
    is_active = fields.Bool()
    location_id = fields.Int(allow_none=True)
