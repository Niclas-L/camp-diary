from db import db
from sqlalchemy.sql import text


def get_diary(id):
    sql = text(
        """SELECT q.question_id, q.question, q.day, d.answer 
        FROM Questions q 
        LEFT JOIN Diary d ON q.question_id = d.question_id 
        WHERE d.user_id = :id 
        ORDER BY q.day;"""
    )
    diary = db.session.execute(sql, {"id": id}).fetchall()
    return diary


# FETCHES OPEN QUESTIONS
def get_questions():
    sql = text("SELECT question FROM questions WHERE visible=TRUE ORDER BY day")
    questions = db.session.execute(sql).fetchall()
    return questions


# FETCHES ALL QUESTIONS
def get_all_questions():
    sql = text("SELECT question_id, question, day FROM questions ORDER BY day")
    result = db.session.execute(sql)
    questions = result.fetchall()
    return questions


# DELETES QUESTION WITH GIVEN ID
def delete_question(question_id):
    sql = text("DELETE FROM questions WHERE question_id=:id")
    db.session.execute(sql, {"id": question_id})
    db.session.commit()


# FETCHES ALL OPEN and UNANSWERED QUESTIONS
def get_unanswered(id):
    sql = text(
        """SELECT q.question_id, q.question, q.day
        FROM Questions q 
        LEFT JOIN Diary d ON q.question_id = d.question_id AND d.user_id = :id 
        JOIN visible_days vd ON q.day = vd.day AND vd.visible = true 
        WHERE d.user_id IS NULL
        ORDER BY q.day;"""
    )
    unanswered = db.session.execute(sql, {"id": id}).fetchall()
    print(unanswered)
    return unanswered


def get_days():
    sql = text("SELECT day, visible FROM visible_days ORDER BY day")
    result = db.session.execute(sql).fetchall()
    return result


def toggle_day(id):
    sql = text("UPDATE visible_days SET visible = NOT visible WHERE day=:id")
    db.session.execute(sql, {"id": id})
    db.session.commit()


def add_question(question, day):
    sql = text("INSERT INTO questions (question, day) VALUES (:question, :day)")
    db.session.execute(sql, {"question": question, "day": day})
    db.session.commit()


def answer_question():
    pass
