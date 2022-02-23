from datetime import date
from flask_restful import Resource, reqparse
from flask import jsonify
from src.db import get_db

parser = reqparse.RequestParser()

class User(Resource):
    def get(self, user_name):
        result = get_db().cursor().execute(f'SELECT * FROM users WHERE username="{user_name}"')
        return dict(zip([c[0] for c in result.description], result.fetchone()))
    
    def post(self):
        parser.add_argument('username')
        parser.add_argument('password')
        data = parser.parse_args()
        un = data['username']
        pw = data['password']
        get_db().cursor().execute(f'INSERT INTO users(id, username, password) VALUES({hash(un)}, "{un}", "{pw}")')
        get_db().commit()
        get_db().close()
        return parser.parse_args()
class Users(Resource):
    def get(self):
        result = get_db().cursor().execute('SELECT * FROM users')
        rows = result.fetchall()
        get_db().close()
        response = []
        for row in rows:
            response.append(dict(zip([c[0] for c in result.description], row)))
        return response