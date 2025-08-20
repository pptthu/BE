from marshmallow import Schema, fields

class ServiceSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    price = fields.Float()
    is_active = fields.Bool()
