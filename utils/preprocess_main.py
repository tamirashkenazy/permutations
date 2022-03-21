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
    """
    Adding each wird from the words file to a file with the name of <sorted_word>.txt in the persistent db
    :param words_file_path: the file with all the words separated by line-break
    :param force_mapping_files: will remove the db dir and re-create it with the files
    :return: None
    """
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
        lines_count = 0
        with open(words_file_path, "r") as all_words_file:
            # read line by line for a very big file
            while line := all_words_file.readline():
                lines_count += 1
                line = line.rstrip()
                add_permutation_to_a_file(persistence_db_dir, line)
        add_number_of_words_to_stats_db(lines_count)

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
