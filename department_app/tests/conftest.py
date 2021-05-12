"""Module contains pytest fixtures to run tests with."""
import pytest
from department_app import create_app, db
from department_app.models.insert_data import populate_db
from config import TestConfig



@pytest.fixture
def app():
    """
    Pytest fixture to make app, application test context
    and db populated with test data available in tests.
    """
    _app = create_app(config_class=TestConfig)
    ctx = _app.test_request_context()
    ctx.push()
    _app.testing = True

    with _app.app_context():
        db.create_all()
        populate_db()

    yield _app
    ctx.pop()


