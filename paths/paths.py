import os.path as path
import os

from db.db_constants import PERMUTATIONS_DB_NAME

BASE_APP_DIR_PATH = path.dirname(path.dirname(__file__))
print(f"BASE_APP_DIR_PATH: {BASE_APP_DIR_PATH}")

DB_DIR = path.join(path.dirname(__file__), "db")


def get_db_dir_path():
    if not path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    return DB_DIR


def get_persistent_db_dir_path():
    permutations_db_dir_path = path.join(
        path.dirname(BASE_APP_DIR_PATH), PERMUTATIONS_DB_NAME
    )
    return permutations_db_dir_path
