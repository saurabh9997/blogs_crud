from marshmallow import fields, Schema, validate


class BlogPostSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(max=255))
    content = fields.String(required=True)
    author = fields.String(required=True, validate=validate.Length(max=100))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
