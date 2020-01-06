#!/usr/bin/env python3
"""
Main application file
"""

__author__ = "Armend Ukehaxhaj"
__version__ = "1.0.0"
__license__ = "MIT"

from logzero import logger
from random import randint
import numpy as np

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
    list_of_tuples = sorted(
        word_stats.items(), key=lambda kv: kv[1], reverse=True)
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
    return output, mapping


def generate_batch(batch_size, skip_num, context_window):
    global index
    # TODO: Remove global value
    index = 4
    assert skip_num <= context_window*2
    assert batch_size % skip_num == 0
    batch = np.ndarray(shape=(batch_size), dtype=np.int32)
    labels = np.ndarray(shape=(batch_size, 1), dtype=np.int32)
    for i in range(batch_size//skip_num):
        seen_words = [data[(index + k) % len(data)]
                      for k in range(0 - context_window, context_window + 1)]
        given_word = seen_words.pop(context_window)
        for j in range(skip_num):
            batch[i*skip_num+j] = given_word
            labels[i*skip_num+j,
                   0] = seen_words.pop(randint(0, len(seen_words) - 1))
        index = (index + 1) % len(data)
    return batch, labels


def main():
    logger.info("Starting app")
    global data
    data, mapping = translate(primary_data_filename, 300)
    # index = 4
    batch, labels = generate_batch(8, 4, 2)
    reverse_mapping = dict(zip(mapping.values(), mapping.keys()))

    for i in range(8):
        logger.info(str.format(
            "{0}: {1}", reverse_mapping[batch[i]], reverse_mapping[labels[i][0]]))


if __name__ == "__main__":
    main()
