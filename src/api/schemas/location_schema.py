from marshmallow import Schema, fields

class LocationSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    address = fields.Str()
