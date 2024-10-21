from flask_restful import reqparse, Resource, request
from models.user import UserModel
import bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity
from middlewares.auth import jwt_required_middleware

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
    
class AuthCurrentUser(Resource):
    @jwt_required_middleware
    def get(self):
        user_id = get_jwt_identity()
        
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"error": "Unauthorized"}, 401
        
        return {
            "id" : user.id,
            "username" : user.username,    
        }, 200
    
    @jwt_required_middleware
    def put(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        
        UserModel.update(id=user_id, username=data['username'])

        return {
            "message": "Successfully updated the username"
        }, 200

    @jwt_required_middleware
    def put(self):
        user_id = get_jwt_identity()
        
        UserModel.delete(id=user_id)

        return {
            "message": "Successfully deleted the user"
        }, 200
        