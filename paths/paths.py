import os.path as path

from db.db_constants import PERMUTATIONS_DB_NAME

BASE_APP_DIR_PATH = path.dirname(path.dirname(path.abspath(__file__)))

def get_persistent_db_dir_path():
    permutations_db_dir_path = path.join(
        path.dirname(path.dirname(BASE_APP_DIR_PATH)), PERMUTATIONS_DB_NAME
    )
    return permutations_db_dir_path
