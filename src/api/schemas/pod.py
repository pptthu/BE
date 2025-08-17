# src/api/schemas/pod.py
from marshmallow import Schema, fields, validate

# Gợi ý giá trị hợp lệ cho status (anh có thể đổi theo hệ thống)
POD_STATUS = ["AVAILABLE", "MAINTENANCE", "UNAVAILABLE"]
"""AVAILABLE" → Pod đang có sẵn để khách đặt.

"MAINTENANCE" → Pod đang bảo trì, tạm thời không thể đặt.

"UNAVAILABLE" → Pod không khả dụng, ví dụ bị lỗi, hoặc ngưng phục vụ."""

class PodCreateRequestSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=255))
    location_id = fields.Int(required=True)   # FK -> locations.id
    price = fields.Float(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(POD_STATUS))

class PodUpdateRequestSchema(Schema):
    name = fields.Str(required=False, validate=validate.Length(min=2, max=255))
    location_id = fields.Int(required=False)
    price = fields.Float(required=False)
    status = fields.Str(required=False, validate=validate.OneOf(POD_STATUS))

class PodResponseSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    location_id = fields.Int(required=True)
    price = fields.Float(required=True)
    status = fields.Str(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)