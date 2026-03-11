# from functools import wraps
# from flask_jwt_extended import verify_jwt_in_request, get_jwt
# from flask import jsonify

# def role_required(required_role):
#     def wrapper(fn):
#         @wraps(fn)
#         def decorator(*args, **kwargs):
#             verify_jwt_in_request(locations=["headers"])
#             claims = get_jwt()

#             if claims.get("role") != required_role:
#                 return jsonify({"message": "Unauthorized access"}), 403

#             return fn(*args, **kwargs)
#         return decorator
#     return wrapper

from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):

            verify_jwt_in_request()

            claims = get_jwt()
            print("JWT CLAIMS:", claims)   # DEBUG LINE

            if claims.get("role") != required_role:
                print("ROLE MISMATCH:", claims.get("role"), required_role)
                return jsonify({"message": "Unauthorized access"}), 403

            return fn(*args, **kwargs)

        return decorator
    return wrapper