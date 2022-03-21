import logging
import sys

import pickledb
import os.path as path

from db.db_constants import (
    STATS_DB_FILE_NAME,
    TOTAL_WORDS_KEY,
    TOTAL_REQUESTS_KEY,
    AVG_PROCESSING_TIME_NS_KEY,
)
from logger.api_logger import get_stream_handler
from paths.paths import get_persistent_db_dir_path


# region Logging
db_logger = logging.getLogger(__name__)
db_logger.setLevel(logging.DEBUG)

db_logger.addHandler(get_stream_handler(sys.stdout, logging.DEBUG))
db_logger.addHandler(get_stream_handler(sys.stderr, logging.ERROR))
# endregion


def get_pickle_db(file_path: str) -> pickledb.PickleDB:
    """
    :param file_path: the path of the pickledb file
    :return: pickleDB object
    """
    db = pickledb.load(file_path, False)
    return db


def init_stats_db(stats_db: pickledb.PickleDB):
    stats_db.set(TOTAL_WORDS_KEY, "0")
    stats_db.set(TOTAL_REQUESTS_KEY, "0")
    stats_db.set(AVG_PROCESSING_TIME_NS_KEY, "0")


def get_stats_db_file_path() -> str:
    persistent_db_path = get_persistent_db_dir_path()
    return path.join(persistent_db_path, STATS_DB_FILE_NAME)


def get_stats_db() -> pickledb.PickleDB:
    stats_db_file_path = get_stats_db_file_path()
    stats_db = pickledb.load(stats_db_file_path, auto_dump=True, sig=False)
    return stats_db


def add_statistics_of_requests(measured_time_nano_sec: int):
    """
    Setting the statistics in the stats.db, setting the number of requests and the avg time for request
    :param measured_time_nano_sec
    :return: None
    """
    db_logger.info(f"Adding statistics of request, ns: {measured_time_nano_sec}")
    stats_db = get_stats_db()
    total_reqs = stats_db.get(TOTAL_REQUESTS_KEY)
    total_reqs = int(total_reqs)
    avg_time_in_ns = stats_db.get(AVG_PROCESSING_TIME_NS_KEY)
    avg_time_in_ns = int(avg_time_in_ns)
    # multiply total_requests with avg time to get total time
    total_time = total_reqs * avg_time_in_ns

    total_time += measured_time_nano_sec
    total_reqs += 1

    # new avg by dividing the total with the number of the requests
    new_avg_time_in_ns = total_time // total_reqs
    stats_db.set(TOTAL_REQUESTS_KEY, str(total_reqs))
    stats_db.set(AVG_PROCESSING_TIME_NS_KEY, str(new_avg_time_in_ns))
    db_logger.info(f"Setting: {TOTAL_REQUESTS_KEY}: {total_reqs}, {AVG_PROCESSING_TIME_NS_KEY}: {new_avg_time_in_ns}")


def add_number_of_words_to_stats_db(number_of_words: int):
    """
    Will add the number of the total words (adding at the preprocessing)
    :param number_of_words
    :return: None
    """
    stats_db = get_stats_db()
    total_words = stats_db.get(TOTAL_WORDS_KEY)
    total_words = int(total_words)
    db_logger.info(f"Setting: {TOTAL_WORDS_KEY}: {total_words}")
    total_words += number_of_words
    stats_db.set(TOTAL_WORDS_KEY, str(total_words))
