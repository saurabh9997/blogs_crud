from functools import wraps

from flask_jwt_extended import get_jwt_identity, jwt_required


def token_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        return fn(current_user, *args, **kwargs)

    return wrapper
