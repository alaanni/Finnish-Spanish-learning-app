from db import db
from flask import session, abort, request
from werkzeug.security import check_password_hash, generate_password_hash
import os

def login(username,password):
    sql = "SELECT password, id, role, level, points FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0], password):
            session["user_id"] = user[1]
            session["user_username"] = username
            session["user_role"] = user[2]
            session["user_level"] = user[3]
            session["user_points"] = user[4]
            session["csrf_token"] = os.urandom(16).hex()
            return True
        else:
            return False

def user_id():
    return session.get("user_id", 0)


def logout():
    del session["user_id"]
    del session["user_username"]
    del session["user_role"]
    del session["user_level"]
    del session["user_points"]


def register(username, password, role):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, role, level, points) VALUES (:username,:password,:role, 0, 0)"
        db.session.execute(sql, {"username":username,"password":hash_value, "role":role, "level":0, "points":0})
        db.session.commit()
    except:
        return False
    return login(username,password)

def require_role(role):
    if role > session.get("user_role", 0):
        abort(403)

def check_points():
    if session.get("user_role", 0) == 2:
        return
    sql = "SELECT points FROM users WHERE id=:user_id"
    points = db.session.execute(sql, {"user_id":user_id()}).fetchone()[0]
    if points > 5 and points <= 10:
        sql = "UPDATE users SET level = 1 WHERE id=:user_id"
    elif points > 10 and points <= 20:
        sql = "UPDATE users SET level = 2 WHERE id=:user_id"
    elif points > 20:
        sql = "UPDATE users SET level = 3 WHERE id=:user_id"
    else: return

    db.session.execute(sql, {"user_id":user_id()})
    db.session.commit()
    session["user_points"] = points

def check_level():
    sql = "SELECT level FROM users WHERE id=:user_id"
    level = db.session.execute(sql, {"user_id":user_id()}).fetchone()[0]
    session["user_level"] = level

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)