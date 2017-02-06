import os

from bottle import TEMPLATE_PATH, route, jinja2_template as template, jinja2_view
from .models import *

from bottle import Bottle

from .config import app


TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), 'templates'))


def generate_csrf_token(length):
    '''Generate a random string using range [a-zA-Z0-9].'''
    chars = string.ascii_letters + string.digits
    return ''.join([choice(chars) for i in range(length)])


def require_csrf(callback, *args, **kwargs):
    import inspect
    callback_args = inspect.getargspec(callback)[0]

    def wrapper(*args, **kwargs):
        token = request.params.csrf_token
        if not token or token != global_vars['csrf_token']:
            abort(400)
        body = callback(*callback_args, **kwargs)
        return body

    return wrapper

global_vars = {'APP_VERSION': pkg_resources.get_distribution('app').version,
               'csrf_token': generate_csrf_token(48)}


j2template = partial(template, template_settings={'globals': global_vars})


@app.route("/protected/")
@require_csrf
def protected_view(db):
    return j2template('protected.html', foo="bar")


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
