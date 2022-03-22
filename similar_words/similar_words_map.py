import logging
import sys
from typing import Dict, List

from similar_words.constants import TOTAL_WORDS_KEY, TOTAL_REQUESTS_KEY, AVG_PROCESSING_TIME_NS_KEY
from logger.api_logger import get_stream_handler
from utils.permutations_utils import sort_a_word


# region Logging
all_words_logger = logging.getLogger(__name__)
all_words_logger.setLevel(logging.DEBUG)

all_words_logger.addHandler(get_stream_handler(sys.stdout, logging.DEBUG))
all_words_logger.addHandler(get_stream_handler(sys.stderr, logging.ERROR))
# endregion


class SimilarWordsMap(object):
    def __init__(self):
        self.stats = {
            TOTAL_WORDS_KEY: 0,
            TOTAL_REQUESTS_KEY: 0,
            AVG_PROCESSING_TIME_NS_KEY: 0,
        }

        self.all_words_map: Dict[str, List[str]] = {}

    def preprocess_mapping_all_words_in_memory(self, all_words_file_path: str):
        """
        Adding each word from the words file to a dictionary with the key of <sorted_word>
        :param all_words_file_path: the file with all the words separated by line-break
        :return: None
        """
        all_words_logger.debug("Mapping all word to a dictionary")
        # if the path does exist and there are no files - try to map the file
        words_count = 0
        with open(all_words_file_path, "r") as all_words_file:
            # read line by line for a very big file
            while line := all_words_file.readline():
                words_count += 1
                line = line.rstrip()
                self.add_word_to_all_words_mapping(line)
        self.add_number_of_words_to_stats(words_count)
        all_words_logger.debug("Finished Mapping all word to db")

    def add_word_to_all_words_mapping(self, word: str):
        sorted_word = sort_a_word(word)
        if sorted_word in self.all_words_map:
            # if key exists - append to list of similar words
            self.all_words_map[sorted_word].append(word)
        else:
            # init list of similar words
            self.all_words_map[sorted_word] = [word]

    def add_number_of_words_to_stats(self, number_of_words: int):
        """
        Will add the number of the total words (adding at the preprocessing)
        :param number_of_words
        :return: None
        """
        all_words_logger.info(f"Adding {number_of_words} to {TOTAL_WORDS_KEY}")
        self.stats[TOTAL_WORDS_KEY] += number_of_words
        all_words_logger.info(f"Total words: {self.stats[TOTAL_WORDS_KEY]}")

    def add_statistics_of_requests(self, measured_time_nano_sec: int):
        """
        Setting the statistics in the stats.db, setting the number of requests and the avg time for request
        :param measured_time_nano_sec
        :return: None
        """
        all_words_logger.info(f"Adding statistics of request, ns: {measured_time_nano_sec}")
        total_reqs = self.stats[TOTAL_REQUESTS_KEY]
        avg_time_in_ns = self.stats[AVG_PROCESSING_TIME_NS_KEY]
        # multiply total_requests with avg time to get total time
        total_time = total_reqs * avg_time_in_ns

        total_time += measured_time_nano_sec
        total_reqs += 1

        # new avg by dividing the total with the number of the requests
        new_avg_time_in_ns = total_time // total_reqs
        self.stats[TOTAL_REQUESTS_KEY] = total_reqs
        self.stats[AVG_PROCESSING_TIME_NS_KEY] = new_avg_time_in_ns
        all_words_logger.info(
            f"Setting: {TOTAL_REQUESTS_KEY}: {total_reqs}, {AVG_PROCESSING_TIME_NS_KEY}: {new_avg_time_in_ns}")

    def get_list_of_permutations(self, word: str) -> List[str]:
        """
        reads the file content of the word similar words.
        :param word: the requested word
        :return: list of similar word
        """
        sorted_word = sort_a_word(word)
        # if the sorted word is not in the map as key, return []
        if sorted_word not in self.all_words_map:
            all_words_logger.info(f"There are no similar words for: {word}")
            return []
        else:
            all_similar_words = self.all_words_map[sorted_word]
            set_of_similar_words = set(all_similar_words)
            if word in set_of_similar_words:
                set_of_similar_words.remove(word)
            all_words_logger.info(f"Got {list(set_of_similar_words)} of similar words for: {word}")
            return list(set_of_similar_words)

    def update_avg_and_reqs_stats(self, measured_time_nano_sec: int):
        """
        Setting the statistics in the stats.db, setting the number of requests and the avg time for request
        :param measured_time_nano_sec
        :return: None
        """
        all_words_logger.info(f"Adding statistics of request, ns: {measured_time_nano_sec}")
        total_reqs = self.stats[TOTAL_REQUESTS_KEY]
        avg_time_in_ns = self.stats[AVG_PROCESSING_TIME_NS_KEY]
        # multiply total_requests with avg time to get total time
        total_time = total_reqs * avg_time_in_ns

        total_time += measured_time_nano_sec
        total_reqs += 1

        # new avg by dividing the total with the number of the requests
        new_avg_time_in_ns = total_time // total_reqs
        self.stats[TOTAL_REQUESTS_KEY] = total_reqs
        self.stats[AVG_PROCESSING_TIME_NS_KEY] = new_avg_time_in_ns
        all_words_logger.info(
            f"Setting: {TOTAL_REQUESTS_KEY}: {total_reqs}, {AVG_PROCESSING_TIME_NS_KEY}: {new_avg_time_in_ns}")

