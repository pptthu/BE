# lọc danh sách booking
from marshmallow import Schema, fields, validate


BOOKING_STATUS = ["PENDING", "CONFIRMED", "CHECKED_IN", "CHECKED_OUT", "CANCELLED"]

class BookingFilterQuerySchema(Schema):
    status = fields.Str(required=False, validate=validate.OneOf(BOOKING_STATUS))
    user_id = fields.Int(required=False)
    pod_id = fields.Int(required=False)

    # Khoảng thời gian ISO8601, ví dụ: 2025-08-20T09:00:00
    date_from = fields.DateTime(required=False)
    date_to   = fields.DateTime(required=False)

    # Phân trang
    page  = fields.Int(required=False, load_default=1, validate=validate.Range(min=1))
    limit = fields.Int(required=False, load_default=20, validate=validate.Range(min=1, max=200))

    # (tuỳ chọn) sắp xếp
    sort_by = fields.Str(required=False, load_default="start_time",
                         validate=validate.OneOf(["start_time", "end_time", "created_at", "updated_at"]))
    sort_dir = fields.Str(required=False, load_default="desc",
                          validate=validate.OneOf(["asc", "desc"]))
