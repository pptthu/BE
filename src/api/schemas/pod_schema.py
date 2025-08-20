from marshmallow import Schema, fields
from src.api.schemas.location_schema import LocationSchema

class PODSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    price = fields.Float()
    status = fields.Str()
    location_id = fields.Int()
    location = fields.Nested(LocationSchema)
