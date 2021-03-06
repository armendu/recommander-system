import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler
from forms import *
from recommander.recommander import Recommander
from functools import wraps
from models import *

# App Config.

app = Flask(__name__)
app.config.from_object('config')
user = {'username': ''}
db = SQLAlchemy(app)


# Automatically tear down SQLAlchemy.
@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        # if 'logged_in' in session:
        if user['username']:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))

    return wrap


@app.route('/', methods=["GET", "POST"])
def home():
    form = UserInputForm(request.form)
    if form.is_submitted and request.method == 'POST':
        search = "%{}%".format(form.user_input.data)
        products = Product.query.filter(Product.name.like(search)).all()

        return render_template('pages/placeholder.home.html',
                               data=user,
                               result=products,
                               form=form)
    return render_template('pages/placeholder.home.html', data=user, form=form)


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html', data=user)


@app.route('/login', methods=["GET", "POST"])
def login():
    """For GET requests, display the login form. 
    For POSTS, login the current user by processing the form.

    """
    form = LoginForm()
    if form.validate_on_submit:
        if form.name.data == "admin" and form.password.data == "123456":
            user['username'] = form.name.data
            return redirect(url_for("home"))
    return render_template("forms/login.html", form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


@app.route('/logout')
def logout():
    user['username'] = ''
    return redirect(url_for("home"))


# @login_required
@app.route('/train')
def train():
    rec = Recommander()
    rec.train()
    return redirect(url_for("home"))


@app.route('/product/<id>')
def get_product(id):
    product_to_show = Product.query.filter_by(id=id).first()

    if not product_to_show:
        pass

    recommandations = []
    recommanded_words = []
    no_w2c_results_to_consider = 4
    no_products_to_recommand = 4
    rec = Recommander()

    # Get the keywords from the name of the product
    product_keywords = product_to_show.name.split()

    for keyword in product_keywords:
        try:
            # Try to find similar words for that keyword
            # Do this until we have enough recommanded words
            # First words get a larger number to consider
            w2v_result = rec.recommand_for(keyword.lower())
            for result in w2v_result[:no_w2c_results_to_consider]:
                recommanded_words.append(result)
                if no_w2c_results_to_consider > 0:
                    no_w2c_results_to_consider -= 1
                else:
                    break
        except Exception as e:
            logging.warning("The following error occurred: " + str(e))

    for word in recommanded_words[:5]:
        search = "%{}%".format(word[0])

        # Get ids of the already added products
        top_recommanded_products_query = Product.query.with_entities(Product.id).filter(
            Product.name.like(search),
            Product.id != id).limit(no_products_to_recommand)

        top_recommanded_products = Product.query.filter(Product.name.like(search), Product.id.notin_(
            top_recommanded_products_query), Product.id!=id).limit(no_products_to_recommand).all()

        if len(top_recommanded_products):
            no_products_to_recommand -= 1

        for product in top_recommanded_products:
            recommandations.append(product)

    return render_template('pages/placeholder.product.html',
                           data=user,
                           product=product_to_show,
                           recommandations=recommandations)



@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


def takeSecond(elem):
    # take second element for sort
    return elem[1]


# Default port:
if __name__ == '__main__':
    app.run()
