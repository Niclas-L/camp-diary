from flask import Flask
from flask import render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password1")
        password2 = request.form.get("password2")
        role = request.form["role"]

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

    return render_template("register.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
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

    return redirect("/")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
