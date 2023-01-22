import sqlite3
from pathlib import Path

def get_db_path() -> Path:
    return Path(__file__).parent / "filepro.db"


def get_db_connection():
    return sqlite3.connect(str(get_db_path()), check_same_thread=False)
