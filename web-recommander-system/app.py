from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
from recommander.recommander import Recommander
import os

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
user = {'username': ''}
# db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/', methods=["GET", "POST"])
def home():
    form = UserInputForm(request.form)
    if form.is_submitted and request.method == 'POST':
        rec = Recommander()
        try:
            result = rec.recommand(form.user_input.data)
        except:
            print("An error occurred")
        # result_to_show = []
        # for word, sim in result[:5]:
        #     result_to_show.append(word)
        return render_template('pages/placeholder.home.html',
                               data=user,
                               result=result[1:6],
                               form=form)
    return render_template('pages/placeholder.home.html', data=user, form=form)


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html', data=user)


@app.route('/train')
def train():
    rec = Recommander()
    rec.train('finalized_model-2.sav')
    return redirect(url_for("home"))


@app.route('/login', methods=["GET", "POST"])
def login():
    """For GET requests, display the login form. 
    For POSTS, login the current user by processing the form.

    """
    form = LoginForm()
    if form.is_submitted:
        # user = User.query.get(form.email.data)
        # if user:
        # if bcrypt.check_password_hash(user.password, form.password.data):
        if form.name.data == "admin" and form.password.data == "123456":
            # user.authenticated = True
            # db.session.add(user)
            # db.session.commit()
            # login_user(user, remember=True)

            # Placeholder user
            user['username'] = form.name.data
            return redirect(url_for("home"))
    return render_template("forms/login.html", form=form)
    # form = LoginForm(request.form)
    # return render_template('forms/login.html', form=form)


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


# Error handlers.


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

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
