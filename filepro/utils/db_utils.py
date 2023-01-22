from filepro.database.database import get_db_connection
from filepro.utils.models import User

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


def get_user_files(user_id):
    cur = con.cursor()
    res = cur.execute(
        """
        SELECT files.uuid, files.filename
        FROM files
        WHERE files.id = ?""",
        (user_id,))
    return res
