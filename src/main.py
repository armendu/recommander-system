#!/usr/bin/env python3
"""
Main application file
"""

__author__ = "Armend Ukehaxhaj"
__version__ = "1.0.0"
__license__ = "MIT"

import math
import random
from logzero import logger
from random import randint
import numpy as np
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

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
    # To define
    skip_num = 6
    context_window = 3
    num_epochs = int(len(data) * context_window / batch_size) + 1

    global data
    data, mapping = translate(primary_data_filename, 300)
    # index = 4
    batch, labels = generate_batch(8, 4, 2)
    reverse_mapping = dict(zip(mapping.values(), mapping.keys()))

    for i in range(8):
        logger.info(str.format(
            "{0}: {1}", reverse_mapping[batch[i]], reverse_mapping[labels[i][0]]))

    # Start with the tensorflow model
    graph = tf.Graph()

    num_samples = 60
    # This uses the CPU initially
    with graph.as_default(), tf.device("/cpu:0"):
        train_inputs = tf.placeholder(dtype=tf.int32, shape=[batch_size])
        train_labels = tf.placeholder(dtype=tf.int32, shape=[batch_size, 1])

        input_weights = tf.Variable(
            tf.random_uniform[mapping_size, hidden_layer_size], -1.0, 1.0)
        output_weights = tf.Variable(tf.truncated_normal(
            [mapping_size, hidden_layer_size], stddev=1.0/math.sqrt(hidden_layer_size)))

        output_baises = tf.Variable(tf.zeros([mapping_size]))

        batch_of_inputs = tf.nn.embedding_lookup(input_weights, train_inputs)
        loss_function = tf.nn.sampled_softmax_loss(
            weights=output_weights, biases=output_baises, labels=train_labels, inputs=batch_of_inputs, num_samples=num_samples)

        final_loss = tf.reduce_mean(loss_function)

        # Define optimizer
        optimizer = tf.train.AdagradeOptimizer(1.1).minimize(final_loss)

        num_validation = 10
        validation_words = np.array(random.sample(range(100), num_validation))

        validation_tf_words = tf.constant(validation_words, dtype=tf.int32)

        normalied_input_weights = input_weights / \
            tf.sqrt(tf.reduce_sum(tf.square(input_weights), 1, True))
        batch_of_validation = tf.nn.embedding_lookup(
            normalied_input_weights, validation_tf_words)
        similar_words = tf.matmu(
            batch_of_validation, tf.transpose(normalied_input_weights))

    with tf.Session(graph=graph) as session:
        tf.global_variables_initilizer().run()
        for epoch in range(num_epochs):
            inputs, labels = generate_batch(batch_size, skip_num, context_window)
            _, loss = session.run([optimizer], {train_inputs:inputs, train_labels: labels})



if __name__ == "__main__":
    main()
