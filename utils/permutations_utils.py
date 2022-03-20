import logging
import os.path as path
from itertools import permutations
from typing import List

from paths.paths import get_persistent_db_dir_path

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def make_all_permutations_from_file(word: str) -> List[str]:
    all_permutations_of_word = ["".join(p) for p in permutations(word)]
    set_of_permutations = set(all_permutations_of_word)
    return list(set_of_permutations)


def sort_a_word(word: str) -> str:
    return "".join(sorted(word))


def get_sorted_word_file_path(dir_path: str, word: str):
    sorted_word = sort_a_word(word)
    word_file_path = path.join(dir_path, f"{sorted_word}.txt")
    return word_file_path


def add_permutation_to_a_file(dir_path: str, word: str):
    word_file_path = get_sorted_word_file_path(dir_path, word)
    with open(word_file_path, "a") as permutation_file:
        permutation_file.write(f"{word}\n")


def get_list_of_permutations_from_a_file(word: str) -> List[str]:
    persistent_db_dir = get_persistent_db_dir_path()
    word_file_path = get_sorted_word_file_path(persistent_db_dir, word)
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


