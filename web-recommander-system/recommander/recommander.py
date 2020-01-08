from logzero import logger
import numpy as np
import pandas as pd
import pickle
from recommander.word2vec import word2vec
from recommander.preprocessor import preprocessor
import os

amazon_sample = "amazon_co-ecommerce_sample.csv"

class Recommander:
    def __init__(self):
        super().__init__()
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        self.BASE_INPUT_DIR = BASE_DIR + "\\input\\"
        self.BASE_MODEL_DIR = BASE_DIR + "\\models\\"

    def open_input_file(self, filename):
        canvas = []
        saved = pd.read_csv(filename)
        canvas = saved['product_name']
        return canvas

    def recommand(self, word):
        model_filename = self.BASE_MODEL_DIR + 'finalized_model-2.sav'

        # Load the pickled model
        w2v_from_pickle = pickle.load(open(model_filename, 'rb'))

        # Use the loaded pickled model to make predictions
        result = w2v_from_pickle.word_sim(word)

        return result

    def train(self, model_name):

        model_filename = self.BASE_MODEL_DIR + model_name
        settings = {}

        # settings['n'] = 5                   # dimension of word embeddings
        # settings['window_size'] = 2         # context window +/- center word
        # settings['min_count'] = 0           # minimum word count
        # settings['epochs'] = 2  # 5000           # number of training epochs
        # # number of negative words to use during training
        # settings['neg_samp'] = 10
        # settings['learning_rate'] = 0.01    # learning rate
        settings['n'] = 5                   # dimension of word embeddings
        settings['window_size'] = 3         # context window +/- center word
        settings['min_count'] = 0           # minimum word count
        settings['epochs'] = 100           # number of training epochs
        # number of negative words to use during training
        settings['neg_samp'] = 10
        settings['learning_rate'] = 0.1    # learning rate
        np.random.seed(0)                   # set the seed for reproducibility

        corpus = self.open_input_file(self.BASE_INPUT_DIR + amazon_sample)

        # Pre process data
        pp = preprocessor()
        corpus = pp.preprocess(corpus)

        # INITIALIZE W2V MODEL
        w2v = word2vec(settings)

        # generate training data
        training_data = w2v.generate_training_data(settings, [corpus])

        # train word2vec model
        w2v.train(training_data)
        
        # save the model to disk
        pickle.dump(w2v, open(model_filename, 'wb'))