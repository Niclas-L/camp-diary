from app import app
from flask import render_template, request, redirect
from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
import auth


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password1")
        password2 = request.form.get("password2")
        role = request.form.get("role")
        auth.register(username, password, password2, role)

    return render_template("register.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    auth.login(username, password)
    return redirect("/")


@app.route("/logout")
def logout():
    auth.logout()
    return redirect("/")
