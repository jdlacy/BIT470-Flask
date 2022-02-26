from src.tools import valid_username, valid_password, encode_auth_token, decode_auth_token
from datetime import datetime
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash
import json
from src.tools import valid_username, valid_password, encode_auth_token, decode_auth_token
from src.db import get_db
from src.const import ENV, SALT
from src.tools import valid_username, valid_password

parser = reqparse.RequestParser()
token_store = []


class Signup(Resource):
    def post(self, credentials):
        try:
            # ARGUMENT PARSING

            # select the arguments to be parsed out of the request (JSON)
            parser.add_argument('username')
            parser.add_argument('password')
            data = parser.parse_args()

            print(data)

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
            uid = hash(data[un])

            # get the secure password hash
            pw_hash = generate_password_hash(str(data['password']) + SALT)
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
                raise Exception("Could not add user to database")

            # CREATE AND RETURN NEW JWT TOKEN
            token = encode_auth_token(un)

            # store the new token in the token store and return it
            token_store[un] = token
            return token

        # ERROR HANDLING
        except Exception as e:
            get_db().close()
            message = getattr(e, 'message', repr(e))
            # if dev or development return error message in JSON
            if (ENV[0.3].lower()) == "dev":
                return json.dumps({"error": getattr(e, 'message', repr(e))}), 401
            else:
                return json.dumps({"error": "Unable to add user"}), 401


class Login(Resource):
    def post(self, credentials):
        # log in to an existing account and generate a new auth token for user
        return 'auth token'
