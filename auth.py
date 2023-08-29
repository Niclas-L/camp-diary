import secrets
from db import db
from flask import session, flash, abort, request
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash


def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        flash("Invalid username or password", category="error")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["id"] = user.id
            session["username"] = username
            session["role"] = user_role()
            session["csrf_token"] = secrets.token_hex(16)

            flash("Logged in successfully!", category="success")
        else:
            flash("Invalid username or password", category="error")


def logout():
    del session["id"]
    del session["username"]
    del session["role"]


def register(username, password, password2, role):
    if len(username) < 3:
        flash("Username must be at least 3 characters long", category="error")
    elif password != password2:
        flash("Passwords do not match", category="error")
    elif len(password) < 4:
        flash("Password must be at least 4 characters long", category="error")
    else:
        flash("Account created successfully!", category="success")
        # add user to database
        hash_value = generate_password_hash(password)
        sql = text(
            "INSERT INTO users (username, password, role) VALUES (:username, :password, :role)"
        )
        db.session.execute(
            sql, {"username": username, "password": hash_value, "role": role}
        )
        db.session.commit()
        return True


def user_role():
    if "username" not in session:
        return None
    sql = text("SELECT role FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": session["username"]})
    return result.fetchone()[0]


def id_role(id: int):
    sql = text("SELECT role FROM users WHERE id=:id")
    role = db.session.execute(sql, {"id": id}).fetchone()
    if role == None:
        return None
    return role[0]


def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
