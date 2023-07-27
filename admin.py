from db import db
from sqlalchemy.sql import text
from flask import flash
import auth


def get_users():
    sql = text("SELECT id, username, role FROM users WHERE role != 'admin'")
    result = db.session.execute(sql)
    our_users = result.fetchall()
    return our_users


def delete_user(user_id):
    sql = text("DELETE FROM users WHERE id=:id")
    db.session.execute(sql, {"id": user_id})
    db.session.commit()


def get_questions():
    sql = text("SELECT question_id, question, day FROM questions ORDER BY day")
    result = db.session.execute(sql)
    questions = result.fetchall()
    return questions


def delete_question(question_id):
    sql = text("DELETE FROM questions WHERE question_id=:id")
    db.session.execute(sql, {"id": question_id})
    db.session.commit()


def assign_participant(p_id, c_id):
    if auth.id_role(p_id) == "participant":
        sql = text(
            "INSERT INTO assigned_participants (user_id, counselor_id) VALUES (:p_id, :c_id)"
        )
        db.session.execute(sql, {"p_id": p_id, "c_id": c_id})
        db.session.commit()
        return True
    else:
        return False