from db import db
from sqlalchemy.sql import text


# FETCHES ALL PARTICIPANTS ASSIGNED TO SPECIFIC COUNSELOR
def get_participants(id):
    sql = text(
        """SELECT ap.participant_id, u.username
        FROM Assigned_participants ap
        LEFT JOIN Users u ON ap.participant_id = u.id
        WHERE ap.counselor_id = :id
        ORDER BY u.username;
        """
    )
    participants = db.session.execute(sql, {"id": id}).fetchall()
    return participants


# CONFIRMS THAT COUNSELOR IS ASSIGNED TO SPECIFIC PARTICIPANT
def is_assigned(counselor_id, participant_id):
    sql = text(
        """SELECT participant_id
        FROM Assigned_participants
        WHERE counselor_id = :counselor_id AND participant_id = :participant_id;
        """
    )
    result = db.session.execute(
        sql, {"participant_id": participant_id, "counselor_id": counselor_id}
    ).fetchone()
    if result[0] == participant_id:
        return True
    return False


# GETS PARTICIPANT'S USERNAME
def get_username(p_id):
    sql = text(
        """SELECT username
        FROM Users
        WHERE id = :p_id;
        """
    )
    result = db.session.execute(sql, {"p_id": p_id}).fetchone()
    return result[0]
