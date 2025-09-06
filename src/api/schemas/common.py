from marshmallow import Schema, fields
class DefaultResponse(Schema):
    ok = fields.Bool(required=True)
    data = fields.Raw()
    error = fields.String()
