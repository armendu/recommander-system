#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Armend Ukehaxhaj"
__version__ = "1.0.0"
__license__ = "MIT"

from logzero import logger

primary_data_filename = "input/Sample.txt"

def count_words(filename):
    word_stats = {}
    with open(filename, "r", encoding="utf-8") as input:
        for line in input.readlines():
            for word in line.split():
                if word in word_stats:
                    word_stats[word] += 1
                else:
                    word_stats[word] = 1
    return word_stats


def get_most_used_words(word_stats: dict, dict_size):
    list_of_tuples = sorted(word_stats.items(), key= lambda kv:kv[1], reverse=True)
    return [kv[0] for kv in list_of_tuples[:dict_size]]


def create_mapping(most_used_words: list):
    mapping = {"UNKNOWN": 0}
    for word in most_used_words:
        mapping[word] = len(mapping)
    return mapping


def translate(filename, dict_size):
    word_stats = count_words(filename)
    most_used_words = get_most_used_words(word_stats, dict_size)
    mapping = create_mapping(most_used_words)
    output = []
    with open(filename, "r", encoding="utf-8") as input:
        for line in input.readlines():
            for word in line.split():
                output.append(mapping.get(word, 0))
    return output

def main():
    logger.info("Starting app")
    result = translate(primary_data_filename, 300)
    logger.info(result)


if __name__ == "__main__":
    main()