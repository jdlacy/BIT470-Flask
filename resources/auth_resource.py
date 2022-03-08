from src.tools import valid_username, valid_password, encode_auth_token, decode_auth_token
from datetime import datetime
from flask import jsonify, request
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
import json
from src.tools import valid_username, valid_password, error_response
from src.token_store import encode_auth_token, decode_auth_token
from src.db import get_db
import src.const
from src.tools import valid_username, valid_password, to_dict, to_dict_array

parser = reqparse.RequestParser()
token_store = dict()


class SignupResource(Resource):
    def post(self):
        try:
            # ARGUMENT PARSING

            # select the arguments to be parsed out of the request (JSON)
            parser.add_argument('user_id')
            parser.add_argument('password')
            data = parser.parse_args()

            # get the parsed argument values
            user_id = str(data['user_id'])
            password= str(data['password'])

            # SANITY CHECKING

            # match returns null if the pattern is not matched
            if not valid_username(user_id):
                raise Exception("Username must begin with a letter and contain only letters, numbers, and underscore")

            # password must contain at least 4 characters
            if not valid_password(password):
                raise Exception("Password does not meet requirements")

            # PREPARE TO INSERT INTO DATABASE

            # get the secure password hash
            password_hash = generate_password_hash(password)
            dt = datetime.utcnow()

            # attempt to insert the new user into the database
            values = (user_id, password_hash, dt)
            query = "INSERT INTO users(user_id, password, date_joined) VALUES (?,?,?)"

            # PERFORM THE INSERT
            try:
                get_db().cursor().execute(query, values)
                get_db().commit()
                get_db().close()
                print("Added user " + user_id + " pw=" + password + "[" + password_hash + "]")
            except Exception as e:
                print(e)
                raise Exception("Could not add user to database")

            # CREATE AND RETURN NEW JWT TOKEN
            # create a new token in the token store and return it
            token = encode_auth_token(user_id)
            resp = make_response({"token": token.decode('utf-8')}, 200)
            resp.headers["Authorization"] = "Bearer " + token.decode('utf-8')
            return resp

        # ERROR HANDLING
        except Exception as e:
            get_db().close()
            return 401


class LoginResource(Resource):
    def post(self):
        # log in to an existing account and generate a new auth token for user
        parser.add_argument('user_id')
        parser.add_argument('password')
        data = parser.parse_args()
        if not ('user_id' in data and 'password' in data):
            return error_response('INVALID', 'Invalid request. userid and password required.', 400)
        user_id = data['user_id']
        password = data['password']

        # get record from the database
        query = 'SELECT * FROM users WHERE user_id=?'
        result = get_db().cursor().execute(query, (user_id,))
        user = to_dict(result.description, result.fetchone())
        if len(user)==0:
            return error_response("NOT_FOUND", "The username and password combination provided was not found", 404)

        if check_password_hash(user['password'], password):
            # encode and store a new token in the token store
            token = encode_auth_token(user_id)
            resp = make_response({"token": token.decode('utf-8')}, 200)
            resp.headers["Authorization"] = "Bearer " + token.decode('utf-8')
            return resp
        else:
            get_db().close()
            return error_response("NOT_FOUND", "The username and password combination provided was not found", 404)

