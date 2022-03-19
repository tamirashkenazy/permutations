import os.path as path
import os

DB_DIR = path.join(path.dirname(__file__), "db")


def get_db_dir_path():
    if not path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    return DB_DIR
