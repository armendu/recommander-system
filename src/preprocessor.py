
import re
import unidecode


class preprocessor():
    def __init__(self):
        self.to_be_converted = [
            {"From": "1", "To": " one "},
            {"From": "2", "To": " two "},
            {"From": "3", "To": " three "},
            {"From": "4", "To": " four "},
            {"From": "5", "To": " five "},
            {"From": "6", "To": " six "},
            {"From": "7", "To": " seven "},
            {"From": "8", "To": " eight "},
            {"From": "9", "To": " nine "},
            {"From": "0", "To": " zero "},
        ]
        pass

    def number_converter(self, word: str):
        for rule in self.to_be_converted:
            word = word.replace(rule["From"], rule["To"])
        return word

    def preprocess(self, input_data: list):
        output = []
        for product in input_data:
            product = str(product)
            product = product.lower()
            product = re.sub(
                r"""[!"$#%&\'()*+,\-./:;<=>?@\[\]^_`{|}~’”“′‘\\]""", " ", product)
            product = unidecode.unidecode(product)
            product = re.sub(" +", " ", product)

            separated_words = product.split()
            for word in separated_words:
                word = self.number_converter(word)
                output.append(word)

        return output
