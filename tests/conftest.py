import pytest, os
from webtest import TestApp

from main import make_app

app = make_app()

@pytest.fixture
def testapp():
    """A fixture to test the web application"""
    yield TestApp(app)
