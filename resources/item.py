from flask_restful import reqparse, request, Resource
from models.item import  ItemModel
from flask_jwt_extended import get_jwt_identity, jwt_required

_user_parser = reqparse.RequestParser()
_user_parser.add_argument("name", type=str, required=True, help= "Name filed cannot be empty")
_user_parser.add_argument("price", type=float, required=True, help= "Price filed cannot be empty")

class ItemById(Resource):
    @jwt_required()
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

class Item(Resource):
    @jwt_required()
    def post(self):
        data = _user_parser.parse_args()
        user_id = get_jwt_identity()
        
        if not user_id:
            return {"error": "Unauthorized"}, 401
        
        item = ItemModel(None, data["name"], data["price"], user_id)
        # Save user to db
        item.save_to_db()
        
        return {"message" : "Item successfully created."}, 201
    
    @jwt_required()
    def get(self):
        name = request.args.get('name')
        items = ItemModel.find_all(name=name)
        return {
            "items" : [item.__dict__ for item in items]
        }, 200