from flask import Flask
from flask_jwt import JWT, jwt_required  # JWT for auth and payload encryption
from flask_restful import Resource, Api, reqparse

from security import identity, authenticate

app = Flask(__name__)
app.secret_key = 'test_key'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth endpoint is built by JWT

items = [
    {'name': "piano", 'price': 200.99},
    {'name': "shoe", 'price': 100.99}
]


class Item(Resource):
    # argument parsing and validation with reqparse
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='price cannot be blank')

    @jwt_required()  # authentication token required
    def get(self, name):
        match = [item for item in items if item['name'] == name]
        return match, 200 if match else 404

    def post(self, name):
        match = [item for item in items if
                 item['name'] == name]  # check if item already exists, returns empty arr if not

        if match:
            return {'message': f'An item with name \'{name}\' already exists'}, 400
        else:
            data = Item.parser.parse_args()
            new_item = {'name': name, 'price': data['price']}
            items.append(new_item)

        return new_item, 201

    def put(self, name):
        data = Item.parser.parse_args()

        item = [item for item in items if
                item['name'] == name]
        if item:
            items[name] = data['price']
        else:
            item = {'name': name, 'price': data['price']}
            items.append(item)

        return item

    def delete(self, name):
        global items
        items = [item for item in items if item['name'] != name]

        return {'message': 'item was deleted'}


class Items(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')  # ex: localhost:5000/item/HikingBoot
api.add_resource(Items, '/items')
app.run(port=5000, debug=True, use_debugger=False)
