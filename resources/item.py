from flask_restful import reqparse, request, Resource
from models.item import  ItemModel
from flask_jwt_extended import get_jwt_identity, jwt_required
from middlewares.auth import jwt_required_middleware

_user_parser = reqparse.RequestParser()
_user_parser.add_argument("name", type=str, required=True, help= "Name filed cannot be empty")
_user_parser.add_argument("price", type=float, required=True, help= "Price filed cannot be empty")

class ItemById(Resource):
    @jwt_required_middleware
    def get(self, item_id):
        item = ItemModel.find_by_id(item_id)
        if not item:
            return {"error": f"Item with id: {item_id} not found"}, 404
        return {
            "id" : item.id,
            "name" : item.name,
            "price" : item.price,
            "owner_id" : item.owner_id
        }, 200
    
    @jwt_required_middleware
    def put(self, item_id):
        data = _user_parser.parse_args()
        user_id = get_jwt_identity()
        ItemModel.update(data["name"], data["price"],item_id, user_id)
        return {
            "message": "Successfully updated the item"
        }, 200
    
    @jwt_required_middleware
    def delete(self, item_id):
        user_id = get_jwt_identity()
        ItemModel.delete(item_id, user_id)
        return {
            "message": "Successfully deleted the item"
        }, 200

class Item(Resource):
    @jwt_required_middleware
    def post(self):
        data = _user_parser.parse_args()
        user_id = get_jwt_identity()
        
        if not user_id:
            return {"error": "Unauthorized"}, 401
        
        item = ItemModel(None, data["name"], data["price"], user_id)
        # Save user to db
        item.save_to_db()
        
        return {"message" : "Item successfully created."}, 201
    
    @jwt_required_middleware
    def get(self):
        name = request.args.get('name')
        items = ItemModel.find_all(name=name)
        return {
            "items" : [item.__dict__ for item in items]
        }, 200