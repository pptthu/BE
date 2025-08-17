# src/api/schemas/service_package.py
from marshmallow import Schema, fields, validate

class ServicePackageCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    description = fields.Str(required=False, allow_none=True)
    price = fields.Float(required=True)  # VND hoặc đơn vị anh chọn

class ServicePackageUpdateSchema(Schema):
    name = fields.Str(required=False, validate=validate.Length(min=2, max=100))
    description = fields.Str(required=False, allow_none=True)
    price = fields.Float(required=False)

class ServicePackageResponseSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=False, allow_none=True)
    price = fields.Float(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)

# Dùng khi đính kèm dịch vụ vào 1 booking (line item)
class BookingServiceItemSchema(Schema):
    service_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))
    unit_price = fields.Float(required=True)  # snapshot giá tại thời điểm đặt
    total_price = fields.Float(required=True)
