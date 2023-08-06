from db import db
from sqlalchemy.sql import text
from collections import defaultdict


# FETCHES ALL DIARY ENTRIES FOR SPECIFIED USER
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


# FETCHES ALL ANSWERS FROM USER, NONE IF QUESTION IS UNANSWERED
def get_answers(id):
    sql = text(
        """SELECT 
                q.question AS question,
                COALESCE(d.answer, 'none') AS answer,
                q.day AS day
            FROM
                questions q
            LEFT JOIN
                diary d ON q.question_id = d.question_id AND d.user_id = :id
            WHERE
                q.visible = TRUE
            ORDER BY
                q.day, q.question_id;"""
    )
    diary = db.session.execute(sql, {"id": id}).fetchall()
    diary_data = defaultdict(list)

    for row in diary:
        diary_data[row[2]].append({"question": row[0], "answer": row[1]})

    return diary_data


# FETCHES ALL DAYS
def get_days():
    sql = text("SELECT day, visible FROM visible_days ORDER BY day")
    result = db.session.execute(sql).fetchall()
    return result


# TOGGLES DAY VISIBILITY
def toggle_day(id):
    sql = text("UPDATE visible_days SET visible = NOT visible WHERE day=:id")
    db.session.execute(sql, {"id": id})
    db.session.commit()


# ADDS QUESTION TO SPECIFIED DAY
def add_question(question, day):
    sql = text("INSERT INTO questions (question, day) VALUES (:question, :day)")
    db.session.execute(sql, {"question": question, "day": day})
    db.session.commit()


# ADDS ENTRY IN DIARY TABLE
def answer_question(p_id, q_id, answer):
    sql = text(
        "INSERT INTO diary (user_id, question_id, answer, date) VALUES (:p_id, :q_id, :answer, current_timestamp)"
    )
    db.session.execute(sql, {"p_id": p_id, "q_id": q_id, "answer": answer})
    db.session.commit()
