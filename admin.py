from db import db
from sqlalchemy.sql import text
from flask import request


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
    sql = text("SELECT question_id, question FROM questions")
    result = db.session.execute(sql)
    questions = result.fetchall()
    return questions


def delete_question(question_id):
    sql = text("DELETE FROM questions WHERE question_id=:id")
    db.session.execute(sql, {"id": question_id})
    db.session.commit()
