About
=====

This is a blueprint for building an extendable web applitcation with BottlePy,
Peewee ORM and Jinja2 template engine. It borrow ideas from a few other
blueprint, but does not bring much. It tries to keep it simple.

Testing is done with PyTest and WebTest.


Getting started
---------------

To get started with the project clone this repository. Create a virtual environment
and then use ``pip`` to install the requirements::

   $ mkvirtualenv --python python3 {{your project name}}
   $ pip install -r requirements.txt
   $ pip install -r test_requirements.txt


No python 2 support ...

Running the application::

   $ make run

That should do ...

Testing
-------

The directory tests contains unit and functional test. In case you wonder
the test directory does not contain ``__init__.py`` because ``py.test``
`explicitly recommends to avoid it <http://doc.pytest.org/en/latest/goodpractices.html>`_.

If you fail to run the tests with ``py.test``, use ``make test`` or install
the project with::

   $ pip install -e .

before running the tests, to run the tests::

   $ make test

