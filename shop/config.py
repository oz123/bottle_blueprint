import os

from bottle import Bottle
from bottle_peewee import Database, Plugin

# This environment variable is set by py-test env
if os.environ.get("TEST_PROJECT"):
    db = Database('test.db', 'peewee.SqliteDatabase', autocommit=False)
else:
    # change this to anything you like
    db = Database('production.db', 'peewee.SqliteDatabase',
                  autocommit=False)

CONFIG = {'db': db}

plugin = Plugin(db)
app = Bottle()
app.install(plugin)

