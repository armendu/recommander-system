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
    
    # logger.info("Preprocessed data: ")
    # logger.info(corpus)

    # INITIALIZE W2V MODEL
    # w2v = word2vec(settings)

    # generate training data
    # training_data = w2v.generate_training_data(settings, [corpus])

    # train word2vec model
    # w2v.train(training_data)

    model_filename = 'models/finalized_model.sav'

    # save the model to disk
    # pickle.dump(w2v, open(model_filename, 'wb'))

    # Load the pickled model
    w2v_from_pickle = pickle.load(open(model_filename, 'rb'))

    # Use the loaded pickled model to make predictions
    w2v_from_pickle.word_sim("star", 10)

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
