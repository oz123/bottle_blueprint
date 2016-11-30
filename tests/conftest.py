import pytest, os
from webtest import TestApp

try:
    from main import make_app
except ImportError:
    print("If you see this, you didn't install the package before running the tests")
    print("Please install the pacakge with 'pip install -e .'")

app = make_app()

@pytest.fixture
def testapp():
    """A fixture to test the web application"""
    yield TestApp(app)
