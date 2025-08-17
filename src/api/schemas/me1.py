# src/api/schemas/me.py
from marshmallow import Schema, fields, validate

class MeResponseSchema(Schema):
    id = fields.Int(required=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    roles_id = fields.Int(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)

class MeUpdateSchema(Schema):
    # PATCH /me → cập nhật profile cơ bản
    username = fields.Str(required=False, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=False)

class MeChangePasswordSchema(Schema):
    # POST /me/change-password
    old_password = fields.Str(required=True)
    new_password = fields.Str(required=True, validate=validate.Length(min=6, max=128))
