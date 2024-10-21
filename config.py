import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super_secret_key"
    JWT_KEY = os.environ.get("JWT_KEY") or "jwt_secret_key"
    DATABASE = os.path.join(os.getcwd(), "data.db")