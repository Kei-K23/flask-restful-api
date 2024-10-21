from flask import Flask
from flask_restful import Api
from security import jwt
from config import Config
from resources.user import UserRegister, UserLogin
from resources.item import Item, ItemById

app = Flask(__name__)
app.config.from_object(Config)

api = Api(app)
jwt.init_app(app)

# Auth routes
api.add_resource(UserRegister, "/api/auth/register")
api.add_resource(UserLogin, "/api/auth/login")
api.add_resource(Item, "/api/items")
api.add_resource(ItemById, "/api/items/<int:item_id>")

if __name__ == '__main__':
    app.run(debug=True)