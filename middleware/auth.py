from flask import request, jsonify, g
import jwt
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()


jwt_secret = os.getenv('JWT_SECRET')


def authenticate(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Verify the JWT token
            payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
            g.user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token is expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return func(*args, **kwargs)

    return decorated
