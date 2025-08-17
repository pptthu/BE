from marshmallow import Schema, fields

class UpdateRoleSchema(Schema):
    role_name = fields.Str(required=True)
