from marshmallow import Schema, fields, validate

# Dùng cho trả danh sách / chi tiết booking
class BookingResponseSchema(Schema):
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    pod_id = fields.Int(required=True)

    # Trả ISO datetime cho client
    start_time = fields.DateTime(required=True)
    end_time   = fields.DateTime(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)

  
    status = fields.Str(required=True, validate=validate.OneOf([
        "pending", "confirmed", "checked_in", "checked_out", "canceled"
    ]))

    # Tiền tệ nên để Decimal -> JSON string để tránh sai số
    total_price = fields.Decimal(as_string=True, allow_none=True)

    # Tuỳ DB có hay không các trường dưới:
    payment_status = fields.Str(allow_none=True)
    check_in_at    = fields.DateTime(allow_none=True)
    check_out_at   = fields.DateTime(allow_none=True)
    checked_in_by  = fields.Int(allow_none=True)
    checked_out_by = fields.Int(allow_none=True)


# (tuỳ chọn) Dùng khi tạo booking (nếu có endpoint create)
class BookingCreateRequestSchema(Schema):
    pod_id = fields.Int(required=True)
    start_time = fields.DateTime(required=True)  
    end_time   = fields.DateTime(required=True)

