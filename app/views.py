import os

from bottle import TEMPLATE_PATH, route, jinja2_template as template, jinja2_view
from .models import *

from bottle import Bottle

from .config import app


TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), 'templates'))


@app.route('/')
def home():
    return template('home.html')


@app.route('/yes/')
@jinja2_view('yes.html')
def yeah():
	return {'title': 'This is cool'}

@app.route('/list/')
def index(db):
    users = User.select()
    result = "".join(["<li>%s</li>" % user.name for user in users])
    return "Here is:<br><ul>%s</ul>" % result
