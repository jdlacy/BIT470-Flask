import sqlite3
from flask import g
from src.const import DB_NAME, DB_DIRECTORY

# Create the SQLite database file and populate it with test users
def init_db():

    try:
        con = sqlite3.connect(DB_DIRECTORY + DB_NAME)
        print('Connected to sqlite:' + DB_NAME)
    except Exception as e:
        print('Error opening database file: ',DB_DIRECTORY + DB_NAME)
        quit()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_DIRECTORY + DB_NAME)
    return db
