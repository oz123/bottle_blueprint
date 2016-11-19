from bottle import Bottle
from bottle_peewee import Database, Plugin
from peewee import Model, CharField

from .config import db


class BaseModel(Model):
    class Meta:
        database = db.database

class User(BaseModel):
    name = CharField()

# feel free to remove this, it's just dummy data
User.create_table(fail_silently=True)
User.create(name='A')
User.create(name='B')
User.create(name='C')

