# src/api/schemas/location.py
from marshmallow import Schema, fields, validate

class LocationRequestSchema(Schema):
    # request dùng khi tạo/cập nhật
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    address = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    # Nếu cần capacity:
    # capacity = fields.Int(required=False)

class LocationSearchQuerySchema(Schema):
    q = fields.Str(required=False)
    page = fields.Int(required=False, load_default=1)
    limit = fields.Int(required=False, load_default=20, validate=validate.Range(min=1, max=200))

class LocationResponseSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    address = fields.Str(required=False, allow_none=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
    # Nếu trả capacity:
    # capacity = fields.Int(required=False, allow_none=True)
