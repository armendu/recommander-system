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

input_path = os.path.abspath(
    os.path.dirname(__file__)) + "\\recommander\\input\\"
input_file = "initial-data.json"


def main():
    """Main entry point for script."""
    with app.app_context():
        db.metadata.create_all(db.engine)

    products_to_add = []

    with open(input_path + input_file) as json_file:
        data = json_file.readlines()
        for line in data:
            obj = json.loads(line)

            prod_title = obj.get("title", "")
            prod_brand = obj.get("brand", "")

            product_to_add = Product(name=prod_title, manufacturer=prod_brand)

            products_to_add.append(product_to_add)

    try:
        db.session.add_all(products_to_add)
        db.session.commit()
        logzero.logger.info("Products added.")
    except Exception as e:
        logzero.logger.error(
            "The following error occurred while adding the Products: " +
            str(e))


if __name__ == '__main__':
    sys.exit(main())