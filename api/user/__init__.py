import sqlite3

from flask import (
    Blueprint, request
)

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route("/", methods=['GET'])
def hello_world():
    cur = cursor_user()

    res = cur.execute("SELECT * FROM user")
    result = res.fetchall()
    return {'users': result}, 200


# get
@bp.route("/<int:id>", methods=['GET'])
def getUserById(id):
    cur = cursor_user()
    res = cur.execute(f'SELECT * FROM user where id = {id} limit 1')
    result = res.fetchone()
    return {'user': result}, 200


# post
@bp.route("/", methods=['POST'])
def createUser():
    error = None
    name = request.form['name']
    login = request.form['login']
    password = request.form['pass']

    con = sqlite3.connect("user.db")
    cur = con.cursor()

    if not name:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'
    elif not login:
        error = 'Login is required.'

    if error is None:
        try:
            cur.execute(
                "INSERT INTO user (name, login, pass) VALUES (?, ?, ?)",
                (name, login, password),
            )
            con.commit()
        except con.IntegrityError:
            error = f"User {name} is already registered."
            return {'message': error}, 500
    else:
        return {'message': error}, 400

    return {'message': 'success'}, 200


@bp.route("/", methods=['PUT'])
def putUser():
    error = None
    id = request.form['id']
    name = request.form['name']

    if not id:
        error = 'Id is empty'
    if not name:
        error = 'Username is required.'

    if error is None:
        con = sqlite3.connect("user.db")
        cur = con.cursor()
        try:
            cur.execute(
                "UPDATE user SET name = ? where id = ?",
                (name, id),
            )
            con.commit()
        except con.Error as err:
            return {'message': err}, 500
    else:
        return {'message': error}, 400

    return {'message': 'success'}, 200


@bp.route("/", methods=['DELETE'])
def deleteUser():
    return {'message': 'success'}, 200


@bp.route("/create_user_db")
def create():
    return create_table_user()


def db_user():
    con = sqlite3.connect("user.db")
    return con


def cursor_user():
    con = db_user()
    cur = con.cursor()
    return cur


def create_table_user():
    try:
        con = sqlite3.connect("user.db")
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT, login text UNIQUE NOT NULL, pass text NOT NULL, name text NOT NULL)")
        cur.execute("""
            INSERT INTO user (login, pass, name) VALUES 
                ('test', 'test', 'test'),
                ('test1', 'test1', 'test1')
        """)
        con.commit()
    except:
        return {'message': 'error'}, 500
    return {'message': 'User db registered'}, 200
