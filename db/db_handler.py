import pickledb
import os.path as path

from db.db_constants import (
    STATS_DB_FILE_NAME,
    TOTAL_WORDS_KEY,
    TOTAL_REQUESTS_KEY,
    AVG_PROCESSING_TIME_NS_KEY,
)
from paths.paths import get_persistent_db_dir_path


def get_pickle_db(file_path: str) -> pickledb.PickleDB:
    db = pickledb.load(file_path, False)
    return db


def init_stats_db(stats_db: pickledb.PickleDB):
    stats_db.set(TOTAL_WORDS_KEY, 0)
    stats_db.set(TOTAL_REQUESTS_KEY, 0)
    stats_db.set(AVG_PROCESSING_TIME_NS_KEY, 0)


def get_stats_db_file_path() -> str:
    return path.join(get_persistent_db_dir_path(), STATS_DB_FILE_NAME)


def get_stats_db() -> pickledb.PickleDB:
    stats_db = pickledb.load(get_stats_db_file_path(), auto_dump=True, sig=False)
    return stats_db


def add_statistics_of_requests(measured_time_nano_sec: int):
    stats_db = get_stats_db()
    total_reqs = stats_db.get(TOTAL_REQUESTS_KEY)
    avg_time_in_ns = stats_db.get(AVG_PROCESSING_TIME_NS_KEY)
    # multiply total_requests with avg time
    total_time = total_reqs * avg_time_in_ns

    total_time += measured_time_nano_sec
    total_reqs += 1

    new_avg_time_in_ns = total_time / total_reqs
    stats_db.set(TOTAL_REQUESTS_KEY, total_reqs)
    stats_db.set(AVG_PROCESSING_TIME_NS_KEY, new_avg_time_in_ns)


def add_number_of_words_to_stats_db(number_of_words: int):
    stats_db = get_stats_db()
    total_words = stats_db.get(TOTAL_WORDS_KEY)
    total_words += number_of_words
    stats_db.set(TOTAL_WORDS_KEY, total_words)
