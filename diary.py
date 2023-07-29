from db import db
from sqlalchemy.sql import text


def get_diary(id):
    sql = text(
        "SELECT q.question_id, q.question, q.day, d.answer FROM Questions q LEFT JOIN Diary d ON q.question_id = d.question_id WHERE d.user_id = :id ORDER BY q.day;"
    )
    diary = db.session.execute(sql, {"id": id}).fetchall()
    return diary


def get_questions():
    sql = text("SELECT question FROM questions WHERE visible=TRUE ORDER BY day")
    questions = db.session.execute(sql).fetchall()
    return questions


# FETCHES ALL OPEN and UNANSWERED QUESTIONS
def get_unanswered(id):
    sql = text(
        """SELECT q.question_id, q.question
        FROM Questions q 
        LEFT JOIN Diary d ON q.question_id = d.question_id AND d.user_id = :id 
        JOIN visible_days vd ON q.day = vd.day AND vd.visible = true 
        WHERE d.user_id IS NULL;"""
    )
    unanswered = db.session.execute(sql, {"id": id}).fetchall()
    return unanswered


def get_days():
    sql = text("SELECT day FROM visible_days WHERE visible = true")
    result = db.session.execute(sql).fetchall()
    return result
