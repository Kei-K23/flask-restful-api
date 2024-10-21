from flask import Flask
from flask_restful import Api
from security import jwt
from config import Config
from resources.user import UserRegister

app = Flask(__name__)
app.config.from_object(Config)

api = Api(app)
jwt.init_app(app)

# Register roues

api.add_resource(UserRegister, "/api/auth/register")

if __name__ == '__main__':
    app.run(debug=True)