from db import db
from flask import session, abort, request
from werkzeug.security import check_password_hash, generate_password_hash
import os

def login(username,password):
    sql = "SELECT password, id, role, level FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0],password):
            session["user_id"] = user[1]
            session["user_username"] = username
            session["user_role"] = user[2]
            session["user_level"] = user[3]
            session["csrf_token"] = os.urandom(16).hex()
            return True
        else:
            return False

def user_id():
    return session.get("user_id",0)


def logout():
    del session["user_id"]
    del session["user_username"]
    del session["user_role"]
    del session["user_level"]


def register(username, password, role, level):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, role, level) VALUES (:username,:password,:role,:level)"
        db.session.execute(sql, {"username":username,"password":hash_value, "role":role, "level":level})
        db.session.commit()
    except:
        return False
    return login(username,password)

def require_role(role):
    if role > session.get("user_role", 0):
        abort(403)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)