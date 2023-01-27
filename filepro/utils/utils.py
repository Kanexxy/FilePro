from filepro.utils.db_utils import get_user_data
from pathlib import Path


def is_logged_in(session) -> bool:
    data = get_user_data(session.get("username"))
    if not data:
        return False
    if data.password != session.get("password"):
        return False
    return True


def get_file_suffix(filename) -> str:
    return Path(filename).suffix
