import uuid
from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from schemas import ProductSchema, ProductEditSchema, ErrorSchema, ErrorEntitySchema
from marshmallow.exceptions import ValidationError

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
swag = Swagger(app)

products = [{'id': uuid.uuid4().hex, 'name': 'Product 1', 'price': 1.5}]


@app.route('/products', methods=['GET'])
@swag_from({
    'tags': ['Products'],
    'responses': {
        200: {
            'schema': ProductSchema
        },
        500: {
            'schema': ErrorSchema
        }
    }
})
def catalog():
    """
    Listing
    """
    return jsonify(products), 200


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
        200: {
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
        data = ProductSchema().load(request.json)
        object_ = dict(ProductSchema().dump(data))
        products.append(object_)

        return jsonify({'data': object_}), 201
    except ValidationError as e:
        print(e)
        errors = {'message': 'Unprocessable Entity.', 'errors': e.messages}

        return jsonify(errors), 422

    except Exception as e:
        print(e)
        return jsonify({'message': 'Internal Server Error'}), 500


@app.route('/products/<string:prod_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Products'],
    'parameters': [{
        'in': 'path',
        'name': 'product_id',
        'required': True
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
    i = 0
    for product in products:
        if prod_id == product['id']:
            del products[i]

            return jsonify({'message': 'No Content'}), 204

        i += 1

    return '', 404


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
def to_edit(product_id):
    """
    Edit
    """

    try:
        object_ = ProductEditSchema().load(request.json)
        data = dict(ProductEditSchema().dump(object_))

        for product in products:
            if product_id == product['id']:
                product.update(**data)

                return jsonify(product), 200

        return jsonify({'message': 'Register Not Found.'}), 404
    except ValidationError as e:
        print(e)
        errors = {'message': 'Unprocessable Entity.', 'errors': e.messages}
        return jsonify(errors), 422
    except Exception as e:
        print(e)
        return jsonify({'message': 'Internal Server Error'}), 500
