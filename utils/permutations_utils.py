import logging
import os.path as path
import time
from itertools import permutations
from typing import List

from shutil import rmtree

from paths.paths import get_db_dir_path

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def make_all_permutations_from_file(word: str) -> List[str]:
    all_permutations_of_word = ["".join(p) for p in permutations(word)]
    set_of_permutations = set(all_permutations_of_word)
    return list(set_of_permutations)


def sort_a_word(word: str) -> str:
    return "".join(sorted(word))


def get_sorted_word_file_path(word: str):
    db_dir_path = get_db_dir_path()
    sorted_word = sort_a_word(word)
    word_file_path = path.join(db_dir_path, f"{sorted_word}.txt")
    return word_file_path


def add_permutation_to_a_file(word: str):
    word_file_path = get_sorted_word_file_path(word)
    with open(word_file_path, "a") as permutation_file:
        permutation_file.write(f"{word}\n")


def preprocess_create_files_from_all_words(words_file_path: str):
    # delete the db_dir
    db_dir = get_db_dir_path()
    rmtree(db_dir)
    with open(words_file_path, "r") as all_words_file:
        lines = all_words_file.readlines()
        # add the number of words to db
        for line in lines:
            line = line.strip()
            add_permutation_to_a_file(line)


def get_list_of_permutations_from_a_file(word: str) -> List[str]:
    word_file_path = get_sorted_word_file_path(word)
    if not path.exists(word_file_path):
        return []
    with open(word_file_path, "r") as word_file:
        lines = word_file.readlines()
        lines = [line.strip() for line in lines]
        # TODO - what to do if the word does not exist in the list
        set_of_words = set(lines)
        if word in set_of_words:
            set_of_words.remove(word)
        return list(set_of_words)


def add_statistics_of_requests(measured_time_nano_sec: int):
    pass


if __name__ == "__main__":
    print("About to start the preprocess")
    start_time = time.time()
    all_words_file_path = path.join(path.dirname(__file__), "words_clean.txt")
    end = time.time()
    preprocess_create_files_from_all_words(all_words_file_path)
    measured_time = end - start_time
    print(f"Finished preprocess in {measured_time:2.2f}")
