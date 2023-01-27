from filepro.database.database import get_db_connection
from filepro.utils.models import User, File
from datetime import datetime

con = get_db_connection()


def create_user(username, password, email):
    statement = """
    INSERT INTO users (username, password, email)
    VALUES (?, ?, ?)"""

    cur = con.cursor()
    cur.execute(statement, (username, password, email))
    con.commit()


def get_user_data(userdata: str):
    cur = con.cursor()
    res = cur.execute(
        """
        SELECT users.id, users.username, users.email, users.password
        FROM users 
        WHERE users.email = ? or users.username = ?""",
        (userdata, userdata))
    res = res.fetchone()
    if not res:
        return None
    return User(*res)


def get_user_files_from_userid(user_id):
    cur = con.cursor()
    res = cur.execute(
        """
        SELECT files.uuid, files.filename
        FROM files
        WHERE files.id = ?""",
        (user_id,))
    return res


def register_file(new_filename, old_filename, userid):
    statement = """
    INSERT INTO files (userid, uuid, filename, upload_date)
    VALUES (?, ?, ?, ?)"""

    cur = con.cursor()
    cur.execute(statement, (userid, new_filename, old_filename, datetime.now()))
    con.commit()


def get_file_name(uuid):
    cur = con.cursor()
    res = cur.execute(
        """
        SELECT * 
        FROM files
        WHERE files.uuid=? """, (uuid,))
    res = res.fetchone()
    if not res:
        return None
    return File(*res)


def get_user_files(username):
    cur = con.cursor()
    res = cur.execute(
        """
        SELECT files.id, files.uuid, files.filename, files.upload_date
        FROM users
        JOIN files ON files.userid = user.id
        WHERE user.username = ?""", (username,))
    if not res:
        return None
    return res.fetchall()
