import json
import re
import jwt
from datetime import datetime, timedelta
from flask import current_app


# STATIC HELPER FUNCTIONS


def toDict(result, row):
    dict(zip([c[0] for c in result.description], row))


def valid_username(user_name):
    # returns true if the is alphanumeric (plus _)and starts with a letter
    un = str(user_name)

    # match returns null if the pattern is not matched
    match = re.match('^[A-Za-z]+[A-Za-z0-9_]{2,15}$', un)
    if match is None:
        return False
    return True


def valid_password(password):
    # returns true if password is at least 4 characters
    pw = str(password)
    return len(pw) >= 4


def decode_auth_token(auth_token):
    try:
        jwt_payload = jwt.decode(
            auth_token,
            current_app.config.get('SECRET_KEY')
        )
        return jwt_payload['sub']
    except jwt.ExpiredSignatureError:
        return json.dumps({'error': 'Signature expired. Please log in again.'})
    except jwt.InvalidTokenError:
        return json.dumps({'error': 'Invalid token. Please log in again.'})


def encode_auth_token(user_name):
    try:
        jwt_payload = {
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'sub': user_name
        }
        return jwt.encode(
            jwt_payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e
