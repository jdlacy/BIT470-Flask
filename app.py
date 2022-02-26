# Sean_Jones
# Jason
# Adam Kohler
# Stephen Gomez-Fox

from flask import Flask
from flask_restful import Resource, Api
from os.path import exists
from src.migrate_db import init_db
from src.const import DB_NAME, DB_DIRECTORY
from flask import g
from resources.user import User, Users
from resources.auth import Signup, Login
import sqlite3

app = Flask(__name__)
app.config.from_object('src.config.DevelopmentConfig')
api = Api(app)

# TODO: move the in-memory token store to the database


# create and populate the database if the db file doesn't exist
if not exists(DB_DIRECTORY + DB_NAME):
    init_db()


# TODO: Replace with intended root get response
class HelloWorld(Resource):
    def get():
        return {'hello': 'world'}





# Associate resource paths with resource classes
api.add_resource(HelloWorld, '/')
api.add_resource(User, '/users/<string:user_name>')
api.add_resource(Users, '/users')
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')


# neatly exit in case of exception
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Run app.py if the current module being run is main.py
if __name__ == '__main__':
    app.run(debug=True)
