from src.tools import valid_username, valid_password, encode_auth_token, decode_auth_token
from datetime import datetime
from flask import jsonify
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
import json
from src.tools import valid_username, valid_password, encode_auth_token, decode_auth_token
from src.db import get_db
import src.const
from src.tools import valid_username, valid_password, to_dict, to_dict_array




tokens = []

def get_token_by_user_id(user_id):
    try:
        return tokens[user_id]
    except:
        print("Token does not exist for user ", user_id)


def get_user_id_from_token(token_hash):
    try:
        for k, v in tokens:
            if v.decode('utf-8') == token_hash:
                print(k, ":", json.dumps(v))
                return k
    except:
        print("Unknown error")

def create_token_for_user_id(user_id):

    token = encode_auth_token(user_id)
    token_store[data['username']] = token
    return token

