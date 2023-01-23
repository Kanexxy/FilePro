from filepro.utils.db_utils import get_user_data


def is_logged_in(session) -> bool:
    data = get_user_data(session.get("username"))
    if not data:
        return False
    if data.password != session.get("password"):
        return False
    return True
