from db import db
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash


def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        print("Invalid username or password")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            print("Logged in successfully!")
            pass
        else:
            print("Invalid username or password")


def logout():
    del session["username"]


def register(username, password, password2, role):
    if len(username) < 3:
        print("Username must be at least 3 characters long")
    elif password != password2:
        print("Passwords do not match")
    elif len(password) < 4:
        print("Password must be at least 4 characters long")
    else:
        print("Account created successfully!")
        # add user to database
        hash_value = generate_password_hash(password)
        sql = text(
            "INSERT INTO users (username, password, role) VALUES (:username, :password, :role)"
        )
        db.session.execute(
            sql, {"username": username, "password": hash_value, "role": role}
        )
        db.session.commit()
