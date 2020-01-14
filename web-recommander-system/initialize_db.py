#!/usr/bin/env python

import sys

import os
import json
import logzero
from flask import Flask
from flask import current_app
from models import Product
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

def main():
    """Main entry point for script."""
    with app.app_context():
        db.metadata.create_all(db.engine)

    products_to_add = []
    input_file = "{0}\\recommander\\input\\{1}".format(app.config["BASEDIR"],app.config[
            "INPUT_TRAINING_FILE"])

    with open(input_file) as json_file:
        data = json_file.readlines()
        for line in data:
            obj = json.loads(line)

            prod_title = obj.get("title", "")
            prod_brand = obj.get("brand", "")
            prod_main_cat = obj.get("main_cat", "")
            prod_description = obj.get("description", "")

            prod_description = get_single_description(prod_description)

            product_to_add = Product(name=prod_title, manufacturer=prod_brand,
                                     main_cat=prod_main_cat, description=prod_description)

            products_to_add.append(product_to_add)

    try:
        db.session.add_all(products_to_add)
        db.session.commit()
        logzero.logger.info("Products added.")
    except Exception as e:
        logzero.logger.error(
            "The following error occurred while adding the Products: " +
            str(e))


def get_single_description(description_array):
    if description_array == "":
        return ""

    if isinstance(description_array, list):
        if len(description_array) == 0:
            return ""

        for item in description_array:
            if item != "":
                return item

    return ""


if __name__ == '__main__':
    sys.exit(main())
