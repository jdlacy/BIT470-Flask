from datetime import datetime
from flask_restful import Resource, reqparse
from flask import jsonify
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from src.db import get_db
import re
import json
from src.const import ENV

# parser used by both User class and Users class
parser = reqparse.RequestParser()

# TODO: Move CRUD operations to functions

class User(Resource):
    def get(self, user_name):

        # retrieves user from database and returns as dict
        # TODO: Require valid auth token to view user data
        try:
            query = 'SELECT * FROM users WHERE username="?"'
            result = get_db().cursor().execute(query, user_name)
            row = result.fetchone()
            return dict(zip([c[0] for c in result.description], row))
        except:
            return dict()


    def post(self):
        # performs an update of an existing user

        # set the arguments to be parsed out of the request (JSON)
        parser.add_argument('username')
        parser.add_argument('password')
        data = parser.parse_args()

        # get the username and password from the parser
        un = str(data['username'])
        pw = str(data['password'])

        # check that username and password are valid format
        if valid_username(un):
            raise Exception("Username must begin with a letter and contain only letters, numbers, and underscore")

        if not valid_password(pw):
            raise Exception("Password does not meet requirements")

        # get the user record from the database
        try:
            query = 'SELECT * FROM users WHERE username="?"'
            result = get_db().cursor().execute(query, un)
            return dict(zip([c[0] for c in result.description], result.fetchone()))
        except Exception as e:
            # return an error if user not found
            return dict(), 400



        # TODO: determine if user id should be updated to new hashed username value

        # get the secure password hash
        pw_hash = generate_password_hash(str(data['password']))
        dt = datetime.utcnow()

        # attempt to update the user into the database
        try:
            values = (un, pw_hash, un)
            query = 'UPDATE users SET username = ?, password = ? WHERE [username = ?]'
            get_db().cursor().execute(query, values)
            get_db().commit()
            get_db().close()
        except Exception as e:
            raise Exception("Could not update the user record")

        # return the user as a dictionary
        return json.dumps({"username": un, "password": "updated"})


class Users(Resource):
    def get(self):

        # TODO: Require valid auth token to retrieve users list
        try:
            result = get_db().cursor().execute('SELECT * FROM users')
            rows = result.fetchall()
            get_db().close()
            response = []
            for row in rows:
                response.append(dict(zip([c[0] for c in result.description], row)))
            return response
        except Exception as e:
            # return an empty dict on error
            return dict(), 400
