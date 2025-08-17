from marshmallow import Schema, fields

class PODSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    price = fields.Decimal(as_string=True)  # DECIMAL(10,2)
    status = fields.Str()
    location_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
