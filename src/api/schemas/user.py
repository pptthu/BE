
from marshmallow import Schema, fields, validate

# ----- Request: tạo mới user -----
class UserCreateRequestSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6, max=128))
    roles_id = fields.Int(required=True)  # FK -> roles.id

# ----- Request: cập nhật user (partial) -----
class UserUpdateRequestSchema(Schema):
    username = fields.Str(required=False, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=False)
    # đổi mật khẩu tách schema riêng để an toàn; nếu muốn cập nhật ở đây thì bật dòng dưới:
    # password = fields.Str(required=False, load_only=True, validate=validate.Length(min=6, max=128))
    roles_id = fields.Int(required=False)

# ----- Request: đổi mật khẩu (tuỳ chọn) -----
class UserChangePasswordRequestSchema(Schema):
    old_password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6, max=128))
    new_password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6, max=128))

# ----- Response: trả về user -----
class UserResponseSchema(Schema):
    id = fields.Int(required=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    roles_id = fields.Int(required=True)          # FK
    role_name = fields.Str(required=False)         # lấy từ roles.name nếu có join
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
