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
import json


primary_data_filename = "input/GoTrainedData.txt"
sample_data_filename = "input/Sample.txt"
amazon_sample = "input/amazon_co-ecommerce_sample.csv"


def open_input_file(filename):
    canvas = []
    
    with open('./input/initial-data.json') as json_file:        
        data = json_file.readlines()
        for line in data:
            obj = json.loads(line)

            value = obj.get("title", "")
            value_brand = obj.get("brand", "")
            temp_sentance = value + " " + value_brand
            # print(temp_sentance)
            
            canvas.append(temp_sentance)
            # if value is not None: 
            #     print(value)
            #     temp_sentance += value
            # if value_brand is not None:
            #     temp_sentance += value_brand
    # canvas = []
    # saved = pd.read_csv(filename)
    # canvas = saved['product_name']
    return canvas


def main():
    logger.info("Starting app")
    settings = {}

    settings['n'] = 5                   # dimension of word embeddings
    settings['window_size'] = 3        # context window +/- center word
    settings['min_count'] = 0           # minimum word count
    settings['epochs'] = 3  # 5000           # number of training epochs
    # number of negative words to use during training
    settings['neg_samp'] = 10
    settings['learning_rate'] = 0.01    # learning rate
    np.random.seed(0)                   # set the seed for reproducibility

    # corpus = [['the', 'quick', 'brown', 'fox',
    #            'jumped', 'over', 'the', 'lazy', 'dog']]
    # logger.info("Retrieving corpus")
    corpus = open_input_file(amazon_sample)

    # Pre process data
    logger.info("Preprocess the data")
    pp = preprocessor()
    corpus = pp.preprocess(corpus)

    # for row in new_corpus:
    #     for word in row:
    #         logger.info(word)
    
    # logger.info("Preprocessed data: ")
    # logger.info(corpus)

    # INITIALIZE W2V MODEL
    # w2v = word2vec(settings)

    # generate training data
    # logger.info("Training")
    # training_data = w2v.generate_training_data(settings, new_corpus)

    # train word2vec model
    # w2v.train(training_data)

    model_filename = 'models/finalized_model-refactored.sav'

    # save the model to disk
    # pickle.dump(w2v, open(model_filename, 'wb'))

    # Load the pickled model
    w2v_from_pickle = pickle.load(open(model_filename, 'rb'))

    # Use the loaded pickled model to make predictions
    w2v_from_pickle.word_sim("microphone", 6)


if __name__ == "__main__":
    main()
