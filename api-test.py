from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from schemas import ProductSchema, ProductEditSchema, ProductCreateSchema, ErrorSchema, ErrorEntitySchema, \
    CategorySchema, CategoryEditSchema
from marshmallow.exceptions import ValidationError
from mongoengine import connect
from models import Product, Category

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
swag = Swagger(app)

# products = [{'id': uuid.uuid4().hex, 'name': 'Product 1', 'price': 1.5}]

connect(
    db='products',
    username='db_username',
    password='db_password',
    host='127.0.0.1',
    port=27017,
    authentication_source='admin'
)


@app.route('/products', methods=['GET'])
@swag_from({
    'tags': ['Products'],
    'responses': {
        200: {
            'schema': ProductSchema
        },
        500: {
            'Internal Error': ErrorSchema
        }
    }
})
def catalog():
    """
    Listing
    """

    try:
        object_ = Product.objects
        data = ProductSchema().dump(object_, many=True)

        return jsonify({'data': data}), 200

    except Exception:

        return 'Internal Server Error', 500


@app.route('/products', methods=['POST'])
@swag_from({
    'tags': ['Products'],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': ProductSchema
    }],
    'responses': {
        201: {
            'schema': ProductSchema
        },
        422: {
            'description': 'Unprocessable Entity.',
            'schema': ErrorEntitySchema
        },
        500: {
            'description': 'Internal Server Error',
            'schema': ErrorSchema
        }
    }
})
def create():
    """
     Create
    """
    try:
        data = ProductCreateSchema().load(request.json)
        cat = Category.objects.get(pk=data['category']) #valida o id
        obj1 = Product(name=data['name'], price=data['price'], category=cat)
        obj1.save()
        data = ProductSchema().dump(obj1)

        return jsonify({'data': data}), 201

    except ValidationError as e:
        errors = {'message': 'Unprocessable Entity.', 'errors': e.messages}

        return jsonify(errors), 422

    except Exception:

        return 'Register Not Found', 404


@app.route('/products/<string:prod_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Products'],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': ProductSchema
    }],
    'responses': {
        204: {
            'description': 'No Response',
            'schema': ErrorSchema
        },
        404: {
            'description': 'Not Found',
            'schema': ErrorSchema
        }
    }
})
def delete(prod_id):
    """
    Delete
    """
    try:
        object_ = Product.objects.get(pk=prod_id)
        Product.delete(object_)

        return '', 204

    except Exception:

        return 'Not Found', 404


@app.route('/products/<string:product_id>', methods=['PATCH'])
@swag_from({
    'tags': ['Products'],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': ProductSchema
    }],
    'responses': {
        200: {
            'schema': ProductEditSchema
        },
        404: {
            'description': 'Not Found',
            'schema': ErrorSchema
        },
        422: {
            'description': 'Unprocessable Entity',
            'schema': ErrorEntitySchema

        },
        500: {
            'description': 'Internal Server Error',
            'schema': ErrorSchema

        }
    }
})
def edit_product(product_id):
    """
    Edit
    """

    try:
        object_ = Product.objects.get(pk=product_id)
        data = ProductSchema().load(request.json)
        object_.update(**data)

        return jsonify({'data': data}), 200

    except ValidationError as e:
        errors = {'message': 'Unprocessable Entity.', 'errors': e.messages}
        return jsonify(errors), 422

    except Exception:

        return 'Register Not Found', 404


# -------------------------- categories----------------------------------------


@app.route('/category', methods=['POST'])
def category_post():
    """
    Create
    """
    try:
        data = CategorySchema().load(request.json)
        object_ = Category(**data)
        object_.save()
        data = dict(CategorySchema().dump(object_))

        return jsonify({'data': data}), 200

    except ValidationError as e:
        errors = {'message': 'Unprocessable Entity.', 'errors': e.messages}

        return jsonify(errors), 422


@app.route('/category', methods=['GET'])
def category_get():
    """
    listing
    """
    object_ = Category.objects
    data = CategorySchema().dump(object_, many=True)

    return jsonify({'data': data}), 200


@app.route('/category/<string:category_id>', methods=['PATCH'])
def category_patch(category_id):
    """
    Edit
    """
    try:
        data = CategoryEditSchema().load(request.json)
        object_ = Category.objects.get(pk=category_id)
        object_.update(**data)

        return jsonify({'data': data}), 200

    except ValidationError as e:
        errors = {'message': 'Unprocessable Entity', 'errors': e.messages}

        return jsonify(errors), 422


@app.route('/category/<string:category_id>', methods=['DELETE'])
def category_delete(category_id):
    """
    Delete
    """
    try:
        object_= Category.objects.get(pk=category_id)
        Category.delete(object_)

        return '', 204

    except Exception:
        return 'Register Not Found', 404
