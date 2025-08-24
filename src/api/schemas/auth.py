# src/api/schemas/auth.py
from marshmallow import Schema, fields, validate

# Request: client gửi username + password để login
class  AuthLoginRequestSchema(Schema):
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=50),
        metadata={"description": "Tên đăng nhập (3-50 ký tự)"}
    )
    password = fields.Str(
        required=True,
        metadata={"description": "Mật khẩu"}
    )

# Response: server trả về token sau khi login thành công
class AuthLoginResponseSchema(Schema):
    access_token = fields.Str(
        required=True,
        metadata={"description": "JWT token hoặc session token"}
    )
    token_type = fields.Str(
        required=True,
        metadata={"description": "Loại token, ví dụ: Bearer"}
    )
    expires_in = fields.Int(
        required=True,
        metadata={"description": "Thời gian hết hạn (giây)"}
    )
