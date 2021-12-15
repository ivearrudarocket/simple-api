from marshmallow import Schema, fields, validate


class CategorySchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True, allow_none=False, validate=validate.Length(min=2, max=50))
    status = fields.Str(required=True, allow_name=False, validate=validate.OneOf(['Active', 'Inative']))

    class Meta:
        fields = ('id', 'name', 'status')
        ordered = True


class CategoryEditSchema(Schema):
    name = fields.String(required=False, allow_none=False, validate=validate.Length(min=2, max=50))
    status = fields.Str(required=False, allow_name=False, validade=validate.OneOf(['Active', 'Inative']))

    class Meta:
        fields = ('name', 'status')
        ordered = True


class ProductSchema(Schema):
    id = fields.String(dump_only=True)
    category = fields.Nested(CategorySchema)
    name = fields.String(required=True, allow_none=False, validate=validate.Length(min=2, max=50))
    price = fields.Float(required=True, allow_none=False, validate=validate.Range(min=0))

    class Meta:
        fields = ('id', 'name', 'price', 'category')
        ordered = True


class ProductCreateSchema(Schema):
    category = fields.String(required=True, allow_none=False)
    name = fields.String(required=True, allow_none=False, validate=validate.Length(min=2, max=50))
    price = fields.Float(required=True, allow_none=False, validate=validate.Range(min=0))


class ProductEditSchema(Schema):
    name = fields.String(required=False, allow_none=False, validate=validate.Length(min=2, max=50))
    price = fields.Float(required=False, allow_none=False, validate=validate.Range(min=0))

    class Meta:
        fields = ('name', 'price')
        ordered = True


class ErrorFieldSchema(Schema):
    field_name = fields.List(fields.String(required=True), required=True)


class ErrorEntitySchema(Schema):
    message = fields.String(required=True, allow_none=False)
    errors = fields.Nested(ErrorFieldSchema, required=True)

    class Meta:
        fields = ('message', 'errors')
        ordered = True


class ErrorSchema(Schema):
    message = fields.String(required=True, allow_none=False)
