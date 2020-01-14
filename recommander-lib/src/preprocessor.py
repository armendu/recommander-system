
import re
import unidecode
import numpy as np


class preprocessor():
    def __init__(self):
        self.to_be_converted = [
            {"From": "1", "To": ""},
            {"From": "3", "To": ""},
            {"From": "2", "To": ""},
            {"From": "4", "To": ""},
            {"From": "5", "To": ""},
            {"From": "6", "To": ""},
            {"From": "7", "To": ""},
            {"From": "8", "To": ""},
            {"From": "9", "To": ""},
            {"From": "0", "To": ""},
        ]
        pass

    def number_converter(self, word: str):
        for rule in self.to_be_converted:
            word = word.replace(rule["From"], rule["To"])
        return word

    def preprocess(self, input_data: list):
        output = []
        for product in input_data:
            placeholder_list = []
            product = str(product)
            product = product.lower()
            product = re.sub(
                r"""[!"$#%&\'()*+,\-./:;<=>?@\[\]^_`{|}~’”“′‘\\]""", " ", product)
            product = unidecode.unidecode(product)
            product = re.sub(" +", " ", product)
            # product = self.number_converter(product)
            separated_words = product.split()

            for word in separated_words:
                if word != '':
                    placeholder_list = np.append(placeholder_list, word)
            
            # print(placeholder_list)
            output.append(placeholder_list)
            
            # print(output)
            
        return output
