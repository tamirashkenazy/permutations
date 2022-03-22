
import logging
import sys
import time
import os.path as path

from logger.api_logger import get_stream_handler
from similar_words.similar_words_map import SimilarWordsMap

BASE_APP_DIR_PATH = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(BASE_APP_DIR_PATH)

# region Logging
preprocess_logger = logging.getLogger(__name__)
preprocess_logger.setLevel(logging.DEBUG)

preprocess_logger.addHandler(get_stream_handler(sys.stdout, logging.DEBUG))
preprocess_logger.addHandler(get_stream_handler(sys.stderr, logging.ERROR))
# endregion


def populate_similar_words() -> SimilarWordsMap:
    """
    populating the dictionary inside the class of SimilarWordsMap by the permutations of a word.
    the key of the dict is the sorted word, and the value is list of permutations
    :return:
    """
    preprocess_logger.info("About to start the preprocess")
    start_time = time.time()
    all_words_file_path = path.join(BASE_APP_DIR_PATH, "words_clean.txt")
    all_words_map = SimilarWordsMap()
    all_words_map.preprocess_mapping_all_words_in_memory(all_words_file_path)
    measured_time = time.time() - start_time
    preprocess_logger.info(f"Finished preprocess in {measured_time:2.2f} seconds")
    return all_words_map