# src/api/schemas/booking_actions.py
from marshmallow import Schema, fields

class BookingActionBaseSchema(Schema):
    # Cho phép gửi ghi chú/ lý do (ví dụ khi cancel)
    note = fields.Str(required=False)

class BookingConfirmSchema(BookingActionBaseSchema):
    pass  # không cần gì thêm, nhưng để tách schema cho rõ

class BookingCancelSchema(BookingActionBaseSchema):
    reason = fields.Str(required=False)

class BookingCheckinSchema(BookingActionBaseSchema):
    # nếu hệ thống cần, có thể cho phép staff ghi thời điểm thực tế
    actual_checkin_at = fields.DateTime(required=False)

class BookingCheckoutSchema(BookingActionBaseSchema):
    actual_checkout_at = fields.DateTime(required=False)
    # (tuỳ chọn) tổng tiền cuối cùng nếu có phát sinh
    final_price = fields.Float(required=False)
