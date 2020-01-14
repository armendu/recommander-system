import os
import pickle
import json
import numpy as np
import pandas as pd
from flask import Flask
from logzero import logger
from recommander.word2vec import word2vec
from recommander.preprocessor import preprocessor

app = Flask(__name__)
app.config.from_object('config')

class Recommander:
    def __init__(self):
        super().__init__()
        base_dir = os.path.abspath(os.path.dirname(__file__))
        
        self.BASE_INPUT_FILE_DIR = base_dir + "\\input\\" + app.config["INPUT_TRAINING_FILE"]
        self.BASE_MODEL_FILE_DIR = base_dir + "\\models\\" + app.config["MODEL_FILENAME"]

    def open_input_file(self):
        canvas = []

        with open(self.BASE_INPUT_FILE_DIR) as json_file:
            data = json_file.readlines()
            for line in data:
                obj = json.loads(line)

                prod_title = obj.get("title", "")
                prod_brand = obj.get("brand", "")
                product_info = prod_title + " " + prod_brand

                canvas.append(product_info)

        return canvas

    def recommand_for(self, word):
        # Load the pickled model
        w2v_from_pickle = pickle.load(open(self.BASE_MODEL_FILE_DIR, 'rb'))

        # Use the loaded pickled model to make predictions
        result = w2v_from_pickle.word_sim(word)

        return result

    def train(self):
        settings = {}

        settings['n'] = 5                   # dimension of word embeddings
        settings['window_size'] = 2         # context window +/- center word
        settings['min_count'] = 0           # minimum word count
        settings['epochs'] = 2  # 5000           # number of training epochs
        # number of negative words to use during training
        settings['neg_samp'] = 10
        settings['learning_rate'] = 0.01    # learning rate
        np.random.seed(0)                   # set the seed for reproducibility

        corpus = self.open_input_file()

        # Pre process data
        pp = preprocessor()
        corpus = pp.preprocess(corpus)

        # INITIALIZE W2V MODEL
        w2v = word2vec(settings)

        # generate training data
        training_data = w2v.generate_training_data(settings, corpus)

        # train word2vec model
        w2v.train(training_data)

        # save the model to disk
        pickle.dump(w2v, open(self.BASE_MODEL_FILE_DIR, 'wb'))