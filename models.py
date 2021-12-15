from mongoengine import Document, FloatField, StringField, ReferenceField


class Product(Document):
    name = StringField(required=True, allow_none=False)
    price = FloatField(required=True, allow_none=False)
    category = ReferenceField('Category', required=True, allow=False)


class Category(Document):
    name = StringField(required=True, allow_none=False)
    status = StringField(required=True, allo_none=False)
