import pytest
import werkzeug
import flask

from backend.db import db as persisting_db
from backend.server.main import create_app
from backend.server.migrations import MODELS


@pytest.fixture(scope="class")
def app() -> flask.Flask:
    """Create a test client for the app"""

    app = create_app("TEST")
    yield app
    with persisting_db.connection_context():
        persisting_db.drop_tables(MODELS, safe=True)
        persisting_db.execute_sql("VACUUM")


@pytest.fixture(scope="class")
def client(app: flask.Flask) -> werkzeug.test.Client:
    return app.test_client()
