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
