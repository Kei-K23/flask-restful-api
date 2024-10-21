from flask_restful import reqparse, Resource
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument("username", type=str, required=True, help= "Username filed cannot be empty")
_user_parser.add_argument("password", type=str, required=True, help= "Password filed cannot be empty")

class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        
        username = data["username"]
        password = data["password"]
        
        if UserModel.find_by_username(username):
            return {"message": "User already exists."}, 400
        print(username, password)
        user = UserModel(None, username, password)
        # Save user to db
        user.save_to_db()
        
        return {"message" : "User successfully created."}, 201
