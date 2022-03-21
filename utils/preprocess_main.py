import os.path as path
import shutil
import time
import os
import sys

# adding the root dir to the sys.path
absolute_project_path = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(absolute_project_path)

from api.api_schema import api_logger
from paths.paths import BASE_APP_DIR_PATH, get_persistent_db_dir_path
from utils.permutations_utils import add_permutation_to_a_file
from db.db_handler import init_stats_db, add_number_of_words_to_stats_db, get_stats_db


def preprocess_create_files_from_all_words(
    words_file_path: str, force_mapping_files: bool = False
):
    persistence_db_dir = get_persistent_db_dir_path()
    if force_mapping_files and path.exists(persistence_db_dir):
        shutil.rmtree(persistence_db_dir)

    if not path.exists(persistence_db_dir):
        os.makedirs(persistence_db_dir)

    is_persistence_dir_empty = len(os.listdir(persistence_db_dir)) == 0

    if is_persistence_dir_empty or force_mapping_files is True:
        api_logger.debug("Mapping all word to db")
        stats_db = get_stats_db()
        init_stats_db(stats_db)
        # if the path does exist and there are no files - try to map the file
        with open(words_file_path, "r") as all_words_file:
            lines = all_words_file.readlines()
            add_number_of_words_to_stats_db(len(lines))
            # add the number of words to db
            for line in lines:
                line = line.strip()
                add_permutation_to_a_file(persistence_db_dir, line)
        api_logger.debug("Finished Mapping all word to db")
    else:
        api_logger.debug("Skipped on mapping the words in files")


if __name__ == "__main__":
    api_logger.info("About to start the preprocess")
    start_time = time.time()
    all_words_file_path = path.join(BASE_APP_DIR_PATH, "words_clean.txt")
    preprocess_create_files_from_all_words(all_words_file_path)
    measured_time = time.time() - start_time
    api_logger.info(f"Finished preprocess in {measured_time:2.2f} seconds")
