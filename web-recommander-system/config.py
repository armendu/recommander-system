import os

# Grabs the folder where the script runs.
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management. You can generate random strings here:
# https://randomkeygen.com/
SECRET_KEY = 'my precious'

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'database.db')

# Set the filename of the model
MODEL_FILENAME = "recommander-model.sav"

# Input file to be used for testing
INPUT_TRAINING_FILE = "shopping-data.json"
