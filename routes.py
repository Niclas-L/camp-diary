from app import app
from flask import render_template, request, redirect, flash
import auth
from admin import get_users, delete_user


@app.route("/", methods=["GET"])
def index():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password1")
        password2 = request.form.get("password2")
        role = request.form.get("role")
        if auth.register(username, password, password2, role):
            return redirect("/")

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


@app.route("/admin")
def admin():
    user_role = auth.user_role()
    if user_role != "admin":
        flash("You do not have permission to view that page", category="error")
        return redirect("/")
    else:
        our_users = get_users()
        return render_template("admin.html", our_users=our_users)


@app.route("/admin/delete/<int:id>", methods=["GET", "POST"])
def admin_delete(id):
    user_role = auth.user_role()
    if user_role != "admin":
        flash("You do not have permission to do that", category="error")
        return redirect("/")
    else:
        delete_user(id)
        return redirect("/admin")
