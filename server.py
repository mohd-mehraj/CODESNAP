from flask import Flask, request
from math import floor
from cockroach import Cockroach
from pony.flask import Pony
from pony.orm import *
from datetime import datetime

db_params = dict(provider='cockroach', user='ayush', host='free-tier6.gcp-asia-southeast1.cockroachlabs.cloud',
                 port=26257, database='shrill-coyote-1394.defaultdb', password="<My Passwor>")


app = Flask(__name__)
app.config.update(dict(
    DEBUG=True,
    PONY=db_params
))
Pony(app)


db = Database()


class User(db.Entity):
    # def __init__(self, table,userid, password, )

    _table_ = 'User'
    user_id = PrimaryKey(str)
    password = Required(str)


class Snippet(db.Entity):
    _table_ = 'Snippets'
    snippetId = PrimaryKey(int)
    user = Required('User')
    snippetText = Required(str)
    snippetLanguage = Required(str)
    imageLink = Required(str)


@db_session  # db_session decorator manages the transactions
def add_snippets(userid, snippetText, snippetLanguage, imagelink):
    Search(user=User.get(user_id=userid), snippetText=snippetText,
           snippetLanguage=snippetLanguage, imageLink=imagelink)


@db_session
def create_user(userid, password):
    User(user_id=userid, password=password)


@app.route('/')  # Home page route
def home_page():
    return "Welcome to CodeSnap!"


active_user = None


@app.route('/login', methods=["POST"])
def login():
    global active_user
    req = request.get_json(force=True, silent=True)
    try:
        user = User.get(user_id=req.get('username'))
        if not user:
            return "UserNotFound"
        # request.args
        # active_user = req.get('username')
        elif user.password != req.get('password'):
            return "Ooops Invalid Password! Please Try again!"
        else:
            active_user = req.get('username')
            return "success"
    except Exception as e:
        return str(e)


@app.route('/register', methods=['POST'])
def signup():
    global active_user
    req = request.get_json(force=True, silent=True)
    username = req.get('username')
    password = req.get('password')
    try:
        user = User.get(user_id=username)
        if not user:
            print('i was here')
            # create_user(userid = user, password = password)
            User(user_id=username, password=password)
            active_user = username
            return "SUCESSS, Your Account has been created successfully"
        else:
            return "FALIURE, Your ID was already taken"
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
