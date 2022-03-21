import os.path as path
from typing import List

from paths.paths import get_persistent_db_dir_path


def sort_a_word(word: str) -> str:
    return "".join(sorted(word))


def get_sorted_word_file_path(dir_path: str, word: str):
    sorted_word = sort_a_word(word)
    word_file_path = path.join(dir_path, f"{sorted_word}.txt")
    return word_file_path


def add_permutation_to_a_file(dir_path: str, word: str):
    """
    adding word to the word file
    :param dir_path: the persistent db path of the files
    :param word: the requested word
    :return: None
    """
    word_file_path = get_sorted_word_file_path(dir_path, word)
    with open(word_file_path, "a") as permutation_file:
        permutation_file.write(f"{word}\n")


def get_list_of_permutations_from_a_file(word: str) -> List[str]:
    """
    reads the file content of the word similar words.
    :param word: the requested word
    :return: list of similar word
    """
    persistent_db_dir = get_persistent_db_dir_path()
    word_file_path = get_sorted_word_file_path(persistent_db_dir, word)
    if not path.exists(word_file_path):
        return []
    with open(word_file_path, "r") as word_file:
        lines = word_file.readlines()
        lines = [line.strip() for line in lines]
        set_of_words = set(lines)
        if word in set_of_words:
            set_of_words.remove(word)
        return list(set_of_words)
