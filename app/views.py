import os
import pkg_resources
import string

from functools import partial
from random import choice

from bottle import (TEMPLATE_PATH,
                    jinja2_template as template, jinja2_view)

from bottle import request, abort, redirect
from .models import User

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

        if request.is_ajax and request.json:
            token = request.json.get("csrf_token")
        else:
            token = request.params.csrf_token
        if not token or token != global_vars['csrf_token']:
            abort(403, 'The form you submitted is invalid or has expired')

        # this is needed for dynamic routes to work with plugins
        [callback_args.pop(callback_args.index(k)) for k in kwargs.keys()]

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


@app.post("/delete/<name:re:\S*>/")
@require_csrf
def delete_device(db, name):
    User.get(User.name == name).delete_instance()
    return redirect("/")


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
