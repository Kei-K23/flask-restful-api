from flask_restful import reqparse, Resource
from models.user import UserModel
import bcrypt
from flask_jwt_extended import create_access_token

_user_parser = reqparse.RequestParser()
_user_parser.add_argument("username", type=str, required=True, help= "Username filed cannot be empty")
_user_parser.add_argument("password", type=str, required=True, help= "Password filed cannot be empty")

class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        
        username = data["username"]
        password = data["password"]
        
        if UserModel.find_by_username(username):
            return {"error": "User is already exist"}, 400

        user = UserModel(None, username, password)
        # Save user to db
        user.save_to_db()
        
        return {"message" : "User successfully created."}, 201

class UserLogin(Resource):
    def post(self):
        data = _user_parser.parse_args()
        
        username = data["username"]
        password = data["password"]
        
        user = UserModel.find_by_username(username)
        is_valid_pwd = bcrypt.checkpw(password.encode("utf-8"), user.password)
        if not user and not is_valid_pwd:
            return {"error": "Unauthorized"}, 401
        
        access_token = create_access_token(identity=user)
        return {"access_token": access_token}, 200
        

        