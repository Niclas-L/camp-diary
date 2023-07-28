from app import app
from flask import render_template, request, redirect, flash, session
import auth
from admin import (
    get_users,
    delete_user,
    get_questions,
    delete_question,
    assign_participant,
)


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
        questions = get_questions()
        return render_template("admin.html", our_users=our_users, questions=questions)


@app.route("/admin/delete/<int:id>", methods=["GET", "POST"])
def admin_delete(id):
    if auth.user_role() != "admin":
        flash("You do not have permission to do that", category="error")
        return redirect("/")
    else:
        delete_user(id)
        return redirect("/admin")


@app.route("/admin/delete/question/<int:id>", methods=["GET", "POST"])
def admin_delete_question(id):
    if auth.user_role() != "admin":
        flash("You do not have permission to do that", category="error")
        return redirect("/")
    else:
        delete_question(id)
        return redirect("/admin")


@app.route("/admin/assign/<int:id>", methods=["GET", "POST"])
def admin_assign(id):
    if auth.user_role() != "admin":
        flash("You do not have permission to do that", category="error")
        return redirect("/")
    else:
        p_id = id
        c_id = request.form.get("counselor")
        if assign_participant(p_id, c_id):
            flash("Participant assigned successfully!", category="success")
        else:
            flash("Something went wrong", category="error")
    return redirect("/admin")


@app.route("/user/<int:id>", methods=["GET", "POST"])
def user_page(id):
    if "username" not in session:
        flash("You must be logged in to view that page", category="error")
        return redirect("/")
    elif session["id"] != id and session["role"] != "admin":
        flash("You do not have permission to view that page", category="error")
        return redirect("/")
    user_id = id
    return render_template("user.html", user_id=user_id)
