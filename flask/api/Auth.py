from functools import wraps

import jwt
from config import Config
from flask import g, jsonify, request
from flask_httpauth import HTTPBasicAuth

from .Model import User

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.check_password(password):
            return False
        g.user = user
        return True


ROLE_PRIORITY = {
    "admin": 3,
    "leader": 2,
    "user": 1
}


def role_required(role):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({"message": "Token is missing"}), 401

            try:
                data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
                user = User.query.filter_by(username=data['username']).first()
                if not user:
                    return jsonify({"message": "Token is invalid"}), 401

                user_role = user.role

                if ROLE_PRIORITY.get(user_role, 0) < ROLE_PRIORITY.get(role, 0):
                    return jsonify({"message": "Token is forbidden"}), 403

                g.user = user

            except jwt.ExpiredSignatureError:
                return jsonify({"message": "Token is expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Token is invalid"}), 401

            return func(*args, **kwargs)

        return decorated_function

    return decorator
