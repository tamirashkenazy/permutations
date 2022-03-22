import logging
import sys
import threading
import unittest

from logger.api_logger import get_stream_handler, FORMATTER_THREADS
from similar_words.constants import TOTAL_REQUESTS_KEY, AVG_PROCESSING_TIME_NS_KEY
from similar_words.similar_words_map import SimilarWordsMap

NUM_OF_THREADS = 100
NUM_OF_UPDATES = 200
AVG_NS = 100000


test_lock_logger = logging.getLogger(__name__)
test_lock_logger.setLevel(logging.DEBUG)

test_lock_logger.addHandler(get_stream_handler(sys.stdout, logging.DEBUG, FORMATTER_THREADS))
test_lock_logger.addHandler(get_stream_handler(sys.stderr, logging.ERROR, FORMATTER_THREADS))

def worker(similar_words_map: SimilarWordsMap):
    for i in range(NUM_OF_UPDATES):
        test_lock_logger.info("Waiting for lock")
        similar_words_map.update_avg_and_reqs_stats(AVG_NS)
        test_lock_logger.info("Released the lock")
    logging.debug('Done')


class UpdateSimilarWordsMapTester(unittest.TestCase):
    def test_update_stats(self):

        similar_words_map = SimilarWordsMap()
        for i in range(NUM_OF_THREADS):
            t = threading.Thread(target=worker, args=(similar_words_map,))
            t.start()

        logging.debug('Waiting for worker threads')
        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()
        self.assertEqual(similar_words_map.stats.get(TOTAL_REQUESTS_KEY), NUM_OF_THREADS * NUM_OF_UPDATES)
        self.assertEqual(similar_words_map.stats.get(AVG_PROCESSING_TIME_NS_KEY), AVG_NS)
