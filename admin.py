from db import db
from sqlalchemy.sql import text
from flask import flash
import auth


def get_users():
    sql = text("SELECT id, username, role FROM users WHERE role != 'admin'")
    result = db.session.execute(sql)
    our_users = result.fetchall()
    return our_users


def get_participants():
    sql = text("SELECT id, username, role FROM users WHERE role = 'participant'")
    result = db.session.execute(sql)
    our_participants = result.fetchall()
    return our_participants


def delete_user(user_id):
    sql = text("DELETE FROM users WHERE id=:id")
    db.session.execute(sql, {"id": user_id})
    db.session.commit()


def assign_participant(p_id, c_id):
    if auth.id_role(p_id) == "participant":
        sql = text(
            "SELECT participant_id FROM assigned_participants WHERE participant_id=:p_id"
        )
        result = db.session.execute(sql, {"p_id": p_id})
        if result.fetchone():
            flash("Participant already assigned", category="error")
            return False

        sql = text(
            "INSERT INTO assigned_participants (participant_id, counselor_id) VALUES (:p_id, :c_id)"
        )
        db.session.execute(sql, {"p_id": p_id, "c_id": c_id})
        db.session.commit()
        return True
    else:
        flash("Something went wrong", category="error")
        return False


def unassign_participant(p_id, c_id):
    if auth.id_role(p_id) == "participant":
        sql = text(
            "DELETE FROM assigned_participants WHERE participant_id=:p_id AND counselor_id=:c_id"
        )
        db.session.execute(sql, {"p_id": p_id, "c_id": c_id})
        db.session.commit()
        return True
    else:
        flash("Something went wrong", category="error")
        return False


def get_assigned():
    sql = text("SELECT participant_id, counselor_id FROM assigned_participants")
    result = db.session.execute(sql)
    assigned = result.fetchall()
    return assigned


def get_assigned_participants():
    sql = text("SELECT participant_id FROM assigned_participants")
    result = db.session.execute(sql)
    assigned_participants = result.fetchall()
    assigned_participants = [x[0] for x in assigned_participants]
    return assigned_participants


def get_counselor_participants():
    sql = text(
        """SELECT ap.counselor_id, u.id, u.username
        FROM assigned_participants ap
        JOIN users u ON ap.participant_id = u.id
        WHERE u.role = 'participant';"""
    )
    result = db.session.execute(sql)
    rows = result.fetchall()
    counselor_participants_list = [(row[0], row[1], row[2]) for row in rows]
    return counselor_participants_list
