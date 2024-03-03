import pytest
import werkzeug
import flask
from typing import Generator

from backend.db import db as persisting_db
from backend.server.main import create_app
from backend.server.auth import jwt_authenticated
from backend.server.migrations import MODELS
from flask import jsonify


@pytest.fixture(scope="class")
def app() -> Generator[flask.Flask, None, None]:
    """Create a test client for the app"""

    app = create_app("TEST")
    yield app
    with persisting_db.connection_context():
        persisting_db.drop_tables(MODELS, safe=True)
        persisting_db.execute_sql("VACUUM")



@pytest.fixture(scope="class")
def client(app: flask.Flask) -> werkzeug.test.Client:
    """
    Create a test client for the app
    """
    return app.test_client()

@pytest.fixture(scope="class")
def client_with_protected_route(app: flask.Flask) -> werkzeug.test.Client:
    """
    Create a test client for the app
    """

    @app.route("/protected", methods=["POST"])
    @jwt_authenticated
    def protected_route(user_id):
        return flask.make_response({"success": user_id}, 200)
    
    return app.test_client()