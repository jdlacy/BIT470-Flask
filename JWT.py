from flask import Flask, jsonify, request, session, flash, render_template
from functools import wraps 
import jwt
import datetime

app = Flask(__NFTAPP__)
app.config['SECRET_KEY'] = 'NFTKEY'

def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token Missing'}), 403
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
                except:
                    return jsonify({'message': 'Token not valid'}), 403
                return func(*args, **kwargs)
            return wrapped

@app.route('/')
def index():
    if not session.get('logged in'):
        else:
            return 'Currently logged in'

@app.route('/public')
def public():
    return 'landing page'

@app.route('/auth')
@check_for_token
def authorised():
    return 'Logged in'

@app.route('/login', methods=[POST])
def login():
    if request.form['username'] and request.form['password'] == 'password':
        session['logged_in'] = True
        token = jwt.encode({
            'user': request.form['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
        },
        app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('utf-8')})
    else:
        return make_response('Not verified', 403, {'WWW-Authenticat': 'authenticate'})