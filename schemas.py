import uuid
from marshmallow import Schema, fields, validate


class ProductSchema(Schema):
    id = fields.UUID(dump_only=True, default=lambda: uuid.uuid4().hex)
    name = fields.String(required=True, allow_none=False, validate=validate.Length(min=2, max=30))
    price = fields.Float(required=True, allow_none=False, validate=validate.Range(min=0))

    class Meta:
        fields = ('id', 'name', 'price')
        ordered = True


class ProductEditSchema(Schema):
    name = fields.String(required=False, allow_none=False, validate=validate.Length(min=2, max=30))
    price = fields.Float(required=False, allow_none=False, validate=validate.Range(min=0))

    class Meta:
        fields = ('name', 'price')
        ordered = True