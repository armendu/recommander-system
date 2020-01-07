#!/usr/bin/env python3
"""
Main application file
"""

__author__ = "Armend Ukehaxhaj"
__version__ = "1.0.0"
__license__ = "MIT"

from logzero import logger
import numpy as np
import pandas as pd
import csv
import pickle
from word2vec import word2vec
from preprocessor import preprocessor


primary_data_filename = "input/GoTrainedData.txt"
sample_data_filename = "input/Sample.txt"
amazon_sample = "input/amazon_co-ecommerce_sample.csv"
# loaded_embeddings = np.load("./Data/MyModel.npy")


def word_counter(filename):
    word_stats = {}
    with open(filename, "r", encoding="utf-8") as file_input:
        for line in file_input.readlines():
            for word in line.split():
                if word in word_stats:
                    word_stats[word] += 1
                else:
                    word_stats[word] = 1
    return word_stats


def read_names():
    with open("./Data/KidNames.csv", "r") as file:
        my_csv = csv.reader(file)
        row_counter = 0
        name_list = []
        for row in my_csv:
            if row_counter == 0:
                row_counter += 1
            else:
                name_list.append(row[0].lower())


def select_most_used_words(word_stats: dict, dict_size):
    list_of_tuples = sorted(
        word_stats.items(), key=lambda kv: kv[1], reverse=True)
    return [kv[0] for kv in list_of_tuples[:dict_size]]


def create_mapping(most_used_words: list):
    mapping = {"UNK": 0}
    for word in most_used_words:
        mapping[word] = len(mapping)
    return mapping


def translate(filename, dict_size):
    word_stats = word_counter(filename)
    most_used_words = select_most_used_words(word_stats, dict_size)
    mapping = create_mapping(most_used_words)
    output = []
    with open(filename, "r", encoding="utf-8") as the_input:
        for line in the_input.readlines():
            for word in line.split():
                output.append(mapping.get(word, 0))
    return output, mapping


def find_similar_words(word):
    embedding = loaded_embeddings[mapping[word]]
    reshaped_embedding = embedding.reshape((embedding.shape[0], 1))
    similarity_vector = np.matmul(loaded_embeddings, reshaped_embedding)
    for sim_word in reversed(similarity_vector.argsort(0)[-10:]):
        print(reverse_mapping[sim_word[0]])


def find_similar_names(name):
    # embedding = sub_embeddings[sub_mapping[name]]
    embedding = loaded_embeddings[mapping[name]]
    reshaped_embedding = embedding.reshape((embedding.shape[0], 1))
    similarity_vector = np.matmul(sub_embeddings, reshaped_embedding)
    for sim_word in reversed(similarity_vector.argsort(0)[-10:]):
        print(sub_reverse_mapping[sim_word[0]])


def open_input_file(filename):
    canvas = []
    saved = pd.read_csv(filename)
    canvas = saved['product_name']
    return canvas


def main():
    logger.info("Starting app")
    settings = {}

    settings['n'] = 5                   # dimension of word embeddings
    settings['window_size'] = 2         # context window +/- center word
    settings['min_count'] = 0           # minimum word count
    settings['epochs'] = 50  # 5000           # number of training epochs
    # number of negative words to use during training
    settings['neg_samp'] = 10
    settings['learning_rate'] = 0.01    # learning rate
    np.random.seed(0)                   # set the seed for reproducibility

    # corpus = [['the', 'quick', 'brown', 'fox',
    #            'jumped', 'over', 'the', 'lazy', 'dog']]
    logger.info("Retrieving corpus")
    corpus = open_input_file(amazon_sample)

    # Pre process data
    logger.info("Preprocess the data")
    pp = preprocessor()
    corpus = pp.preprocess(corpus)

    # INITIALIZE W2V MODEL
    w2v = word2vec(settings)

    # generate training data
    training_data = w2v.generate_training_data(settings, [corpus])

    # train word2vec model
    w2v.train(training_data)

    model_filename = 'models/finalized_model.sav'

    # save the model to disk
    pickle.dump(w2v, open(model_filename, 'wb'))

    # Load the pickled model
    w2v_from_pickle = pickle.load(open(model_filename, 'rb'))

    # Use the loaded pickled model to make predictions
    w2v_from_pickle.word_sim("play", 3)

    # w2v.word_sim("wars", 3)

    # global data
    # data, mapping = translate(primary_data_filename, 300)
    # # index = 4
    # batch, labels = generate_batch(8, 4, 2)
    # reverse_mapping = dict(zip(mapping.values(), mapping.keys()))

    # sub_mapping = {}

    # sub_reverse_mapping = {}
    # sub_embeddings = []
    # for k, v in mapping.items():
    #     if k in name_list:
    #         sub_mapping[k] = len(sub_embeddings)
    #         sub_reverse_mapping[len(sub_embeddings)] = k
    #         sub_embeddings.append(loaded_embeddings[v])
    # sub_embeddings = np.array(sub_embeddings)

    # for i in range(8):
    #     logger.info(str.format(
    #         "{0}: {1}", reverse_mapping[batch[i]], reverse_mapping[labels[i][0]]))


if __name__ == "__main__":
    main()
