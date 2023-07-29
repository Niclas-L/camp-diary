from db import db
from sqlalchemy.sql import text


def get_diary(id):
    sql = text(
        "SELECT q.question_id, q.question, d.answer FROM Questions q LEFT JOIN Diary d ON q.question_id = d.question_id WHERE d.user_id = :id;"
    )
    diary = db.session.execute(sql, {"id": id}).fetchall()
    return diary


def get_questions():
    sql = text("SELECT question FROM questions WHERE visible=TRUE ORDER BY day")
    questions = db.session.execute(sql).fetchall()
    return questions


def get_unanswered(id):
    sql = text(
        "SELECT q.question_id, q.question FROM Questions q LEFT JOIN Diary d ON q.question_id = d.question_id AND d.user_id = :id WHERE d.user_id IS NULL;"
    )
    unanswered = db.session.execute(sql, {"id": id}).fetchall()
    return unanswered
