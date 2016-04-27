import os
from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'this_will_be_changed'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')
app.config.from_pyfile('config.py')
# app.config.(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
bootstrap=Bootstrap(app)
# from models import Result

class NameForm(Form):
  name = StringField('What is your name?', validators = [DataRequired()])
  submit = SubmitField('Submit')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Name %r>' % self.name

@app.route('/', methods=('GET', 'POST'))
def index():
  form = NameForm()
  if form.validate_on_submit():
    old_name = session.get('name')
    if old_name is not None and old_name != form.name.data:
      flash('Looks like you have changed your name!')
    session['name'] = form.name.data
    form.name.data = ''
    return redirect(url_for('index'))
  return render_template('index.html', form=form, name=session.get('name'))

@app.route('/about')
def about():
  return  render_template('about.html')

@app.route('/user/<name>', methods=['GET', 'POST'])
def user(name):
  # name = None
  form = NameForm()
  if form.validate_on_submit():
      name = form.name.data
      form.name.data = ''
  return render_template('user.html', form=form, name=name)


@app.route('/json')
def json():
    return """{'foo':{'bar': 'hello'}}"""


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
  app.run(debug=True)