from app import app
from flask import render_template, request, redirect, flash, session
import auth
import diary
from admin import (
    get_users,
    get_participants,
    delete_user,
    assign_participant,
    get_assigned,
    get_assigned_participants,
    get_counselor_participants,
    unassign_participant,
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
            auth.login(username, password)
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


@app.route("/admin/manage-users")
def admin():
    user_role = auth.user_role()
    if user_role != "admin":
        flash("You do not have permission to view that page", category="error")
        return redirect("/")
    else:
        print(get_counselor_participants())
        return render_template(
            "manage-users.html",
            our_users=get_users(),
            our_participants=get_participants(),
            questions=diary.get_all_questions(),
            assigned=get_assigned(),
            assigned_participants=get_assigned_participants(),
            counselor_participants=get_counselor_participants(),
        )


@app.route("/admin/delete/<int:id>", methods=["GET", "POST"])
def admin_delete(id):
    if auth.user_role() != "admin":
        flash("You do not have permission to do that", category="error")
        return redirect("/")
    else:
        delete_user(id)
        return redirect("/admin/manage-users")


@app.route("/admin/assign/<int:id>", methods=["GET", "POST"])
def admin_assign(id):
    if auth.user_role() != "admin":
        flash("You do not have permission to do that", category="error")
        return redirect("/")
    else:
        selected_participants = request.form.getlist("selected_participants[]")
        c_id = id
        success = True
        for p_id in selected_participants:
            if not assign_participant(p_id, c_id):
                success = False
        if success:
            flash("Participant(s) assigned successfully!", category="success")
    return redirect("/admin/manage-users")


@app.route("/admin/unassign/<int:id>", methods=["GET", "POST"])
def admin_unassign(id):
    if auth.user_role() != "admin":
        flash("You do not have permission to do that", category="error")
        return redirect("/")
    else:
        selected_participants = request.form.getlist("selected_participants[]")
        c_id = id
        success = True
        for p_id in selected_participants:
            if not unassign_participant(p_id, c_id):
                success = False
        if success:
            flash("Participant(s) unassigned successfully!", category="success")
    return redirect("/admin/manage-users")


@app.route("/admin/manage-diary")
def manage_diary():
    if auth.user_role() != "admin":
        flash("You do not have permission to do that", category="error")
        return redirect("/")
    else:
        questions = diary.get_all_questions()
        days = diary.get_days()
        return render_template("manage-diary.html", questions=questions, days=days)


@app.route("/admin/add/question/<int:day>", methods=["GET", "POST"])
def add_question(day):
    if auth.user_role() != "admin":
        flash("You do not have permission to do that", category="error")
        return redirect("/")
    else:
        question = request.form.get("question")
        diary.add_question(question, day)
        return redirect("/admin/manage-diary")


@app.route("/admin/delete/question/<int:id>", methods=["GET", "POST"])
def delete_question(id):
    if auth.user_role() != "admin":
        flash("You do not have permission to do that", category="error")
        return redirect("/")
    else:
        diary.delete_question(id)
        return redirect("/admin/manage-diary")


@app.route("/admin/toggle-day/<int:id>")
def toggle_day(id):
    if auth.user_role() != "admin":
        flash("You do not have permission to do that", category="error")
        return redirect("/")
    else:
        diary.toggle_day(id)
        return redirect("/admin/manage-diary")


@app.route("/user/<int:id>")
def user_page(id):
    if "username" not in session:
        flash("You must be logged in to view that page", category="error")
        return redirect("/")
    if session["id"] != id and session["role"] != "admin":
        flash("You do not have permission to do that")
        return redirect("/")

    if session["role"] == "participant":
        diary_data = diary.get_answers(id)
        for day, entries in diary_data.items():
            print("day:", day, "| entries:", entries)
        return render_template("participant.html", diary_data=diary.get_answers(id))
    else:
        return render_template("user.html", user_id=id)


@app.route("/participant/answer/<int:q_id>", methods=["GET", "POST"])
def answer_question(q_id):
    if auth.user_role() != "participant":
        flash("You do not have permission to do that", category="error")
        return redirect("/")
    else:
        answer = request.form.get("answer")
        if answer == "":
            flash("You must provide an answer", category="error")
            return redirect(f"/user/{session['id']}")
        diary.answer_question(session["id"], q_id, answer)
        return redirect(f"/user/{session['id']}")
