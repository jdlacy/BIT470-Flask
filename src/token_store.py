from datetime import datetime, timedelta
from flask import jsonify, current_app, request
import json
import jwt

# TODO: compare jwt, flask_jwt_extended (flask_jwt abandoned)

from src.tools import valid_username, valid_password
from src.db import get_db
import src.const
from src.tools import valid_username, valid_password, to_dict, to_dict_array

tokens = []


# return the current valid tokan
# ALWAYS ADD THIS IN THE TO THE AUTHORIZATION HEADER OF ANY RESPONSE
def jwt_current_token(user_id):
    try:
        return tokens[user_id]
    except:
        print("Token does not exist for user ", user_id)


# decode a token and return the user id
def jwt_user_id(token):
    # errors handled in called function
    decoded = decode_auth_token(token)
    return decoded["sub"]


def encode_auth_token(user_id):
    try:
        jwt_payload = {
            "iss": "nftgram",
            "sub": user_id,
            "role": "user" if user_id != "admin" else "admin",
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
        }
        return jwt.encode(jwt_payload, current_app.config.get('SECRET_KEY'), algorithm='HS256')

    except Exception as e:
        return e


def decode_auth_token(token):
    try:
        # decode the token using SECRET_KEY from config.py
        jwt_payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
        user_id = jwt("sub")
        # did not trigger expired except, extend time with new token
        tokens[user_id] = encode_auth_token(user_id)
        return jwt_payload

    # TODO: handle actual errors
    except jwt.ExpiredSignatureError:
        return json.dumps({'error': 'Signature expired. Please log in again.'})
    except jwt.InvalidTokenError:
        return json.dumps({'error': 'Invalid token. Please log in again.'})


def get_token_from_header(req):
    auth = req.headers.get('Authorization')
    if auth is None: return None
    token = auth[7, ]
    return token


def get_user_from_header(req):
    token = get_token_from_header(req)
    if token is None: return None
    return jwt_user_id(token)



