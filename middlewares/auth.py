from functools import wraps
from flask_jwt_extended import verify_jwt_in_request

def jwt_required_middleware(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            # If the token is missing or invalid, return an error response
            return {"message": "Missing or invalid JWT token", "error": str(e)}, 401

        return fn(*args, **kwargs)
    
    return wrapper