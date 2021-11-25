import uuid
from flask import Flask, jsonify, request

app = Flask(__name__)
products = [
    {'id': uuid.uuid4().hex, 'name': 'First Product', 'price': 12.0},
    {'id': uuid.uuid4().hex, 'name': 'second Product', 'price': 35.0},
    {'id': uuid.uuid4().hex, 'name': 'third Product', 'price': 30.0}
]


@app.route('/products', methods=['GET'])
def catalog():
    return jsonify(products)


@app.route('/products', methods=['POST'])
def create():

    product = request.json
    products.append(product)

    return jsonify(product)


@app.route('/products/<int:prod_id>', methods=['DELETE'])
def delete(prod_id):
    i = 0

    for product in products:
        if prod_id == product['id']:
            del products[i]

            return '', 204

        i += 1

    return '', 404


@app.route('/products/<int:prod_id>', methods=['PATCH'])
def to_edit(prod_id):
    i = 0

    for product in products:
        if prod_id == product['id']:
            y = request.json
            del products[i]
            products.insert(i, y)

            return '', 200

        i += 1

    return '', 404
