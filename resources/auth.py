from src.tools import valid_username, valid_password, encode_auth_token, decode_auth_token
from datetime import datetime
from flask import jsonify
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash
import json
from src.tools import valid_username, valid_password, encode_auth_token, decode_auth_token
from src.db import get_db
from src.const import ENV, SALT
from src.tools import valid_username, valid_password

parser = reqparse.RequestParser()
token_store = dict()


class Signup(Resource):
    def post(self):
        try:
            # ARGUMENT PARSING

            # select the arguments to be parsed out of the request (JSON)
            parser.add_argument('username')
            parser.add_argument('password')
            data = parser.parse_args()

            # get the parsed argument values
            un = str(data['username'])
            pw = str(data['password'])

            # SANITY CHECKING

            # match returns null if the pattern is not matched
            if not valid_username(un):
                raise Exception("Username must begin with a letter and contain only letters, numbers, and underscore")

            # password must contain at least 4 characters
            if not valid_password(pw):
                raise Exception("Password does not meet requirements")

            # PREPARE TO INSERT INTO DATABASE
            # user id is an integer hash of the username
            uid = hash(un)

            # get the secure password hash
            pw_hash = generate_password_hash(pw + SALT)
            dt = datetime.utcnow()

            # attempt to insert the new user into the database
            values = (uid, un, pw_hash, dt)
            query = "INSERT INTO users(id, username, password, date_joined) VALUES (?,?,?,?)"

            # PERFORM THE INSERT
            try:
                get_db().cursor().execute(query, values)
                get_db().commit()
                get_db().close()
            except Exception as e:
                print(e)
                raise Exception("Could not add user to database")

            # CREATE AND RETURN NEW JWT TOKEN
            token = encode_auth_token(un)

            # store the new token in the token store and return it
            token_store[un] = token
            return jsonify({"token": token.decode('utf-8')})

        # ERROR HANDLING
        except Exception as e:
            get_db().close()
            return 401


class Login(Resource):
    def post(self):
        # log in to an existing account and generate a new auth token for user
        parser.add_argument('username')
        parser.add_argument('password')
        data = parser.parse_args()

        un = str(data['username'])

        query = 'SELECT * FROM users WHERE username=?'
        result = get_db().cursor().execute(query, (un,))
        user = dict(zip([c[0] for c in result.description], result.fetchone()))

        pw = str(data['password'])
        pw_hash = generate_password_hash(pw + SALT)
        db_hash = user['password']

        if db_hash == db_password:
            token = encode_auth_token(un)
            token_store[un] = token
            return jsonify({"token": token.decode('utf-8')})
        else:
            get_db().close()
            return 401
