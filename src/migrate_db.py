import sqlite3
from os import path, getcwd
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from src.const import DB_NAME, SALT, DB_USERS, DB_DIRECTORY

# Create the SQLite database file and populate it with test users
def init_db():
    print("cwd = " + path.dirname(getcwd()))
    print("DB_DIRECTORY = " + DB_DIRECTORY)

    try:
        con = sqlite3.connect(DB_DIRECTORY + DB_NAME)
        print('Connected to sqlite:' + DB_NAME)
    except Exception as e:
        print('Unable to create database file ' + DB_NAME)
        quit();

    # Get a cursor object needed to execute queries
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER NOT NULL, username text PRIMARY KEY, password text, date_joined Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')

    # Parameterized SQL Query String for adding users
    query = "INSERT OR IGNORE INTO users VALUES (?,?,?,?)"

    # Insert users
    for user in DB_USERS:
        # values expanded out into variables for easier code reading
        id = hash(user[0])
        un = user[0]
        pw = generate_password_hash(user[1] + SALT)
        dt = datetime.utcnow()
        values = (id, un, pw, dt)
        try:
            cur.execute(query, values)
            print("Success: Added user ", values)
        except:
            print('Error: Unable to add user ', values)

    # commit changes to the database and close the connection
    con.commit()
    con.close()
