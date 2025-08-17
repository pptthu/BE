from marshmallow import Schema, fields

class TodoRequestSchema(Schema):
    title = fields.Str(required=True)

class TodoResponseSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    created_at = fields.DateTime()
