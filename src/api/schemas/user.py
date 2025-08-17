from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int()
    full_name = fields.Str()
    email = fields.Email()
    role_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
