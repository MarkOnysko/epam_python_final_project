"""Module contains pytest fixtures to run tests with."""
import threading
import time

import pytest
from flask import request

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


@pytest.fixture
def client(app):
    """
    A pytest fixture to make a test client available
    in tests.
    """
    client = app.test_client()
    yield client


@pytest.fixture(scope="module")
def module_app():
    """
    Pytest fixture to make app, application test context
    and db populated with test data available in tests.
    Module scope to make server work in view tests.
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


@pytest.fixture(scope="module")
def mclient(module_app):
    """
    A pytest fixture to make a test client available
    in tests. Module scope to make server work in view tests.
    """
    client = module_app.test_client()
    yield client


def shutdown_server():
    """
    Helper function to shut down the test server in the "server"
    pytest fixture.
    """
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


@pytest.fixture(scope="module")
def server(module_app):
    """
    Pytest fixture to make app running ass a server during
    test. This makes possible to send requests from view functions
    to api endpoints in tests.
    """

    @module_app.route("/shutdown", methods=("POST",))
    def shutdown():
        shutdown_server()
        return "Shutting down server ..."

    t = threading.Thread(target=module_app.run)
    time.sleep(5)
    yield t.start()

    import requests

    requests.post("http://localhost:5000/shutdown")
