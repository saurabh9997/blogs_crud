from marshmallow import fields, Schema, validate


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(max=100))
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=8))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
