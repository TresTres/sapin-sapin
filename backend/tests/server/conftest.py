import pytest
import werkzeug
import flask
import jwt
from typing import Generator, Dict

from backend.db import db as persisting_db
from backend.server.main import create_app
from backend.server.auth import jwt_authenticated
from backend.server.migrations import MODELS
from backend.models import User, DataEventSeries, DataEvent
from tests.constants import *


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


@pytest.fixture(scope="class")
def valid_user_token_header(
    client: werkzeug.test.Client,
) -> Dict[str, str]:
    """
    Create a valid bearer token for a user
    """
    token = jwt.encode(
        {
            "user": VALID_USER_ID,
            "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15),
        },
        key=client.application.config["ACCESS_KEY_SECRET"],
        algorithm="HS256",
        headers={"typ": "JWT"},
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def client_with_user(
    client: werkzeug.test.Client,
) -> Generator[werkzeug.test.Client, None, None]:
    """
    Create a user for testing
    """
    with persisting_db.connection_context():
        User.create(
            id=VALID_USER_ID,
            username=VALID_USERNAME,
            email=VALID_EMAIL,
            password=VALID_PASSWORD,
            date_joined=VALID_JOIN_DATE,
        )
    yield client
    with persisting_db.connection_context():
        User.truncate_table()
        DataEventSeries.truncate_table()


@pytest.fixture(scope="function")
def client_with_data_series(
    client_with_user: werkzeug.test.Client,
) -> Generator[werkzeug.test.Client, None, None]:
    """
    Create a user for testing
    """
    with persisting_db.connection_context():
        DataEventSeries.create(
            id=VALID_SERIES_ID,
            owner=User.get(User.id == VALID_USER_ID),
            title=VALID_SERIES_TITLE,
            description=VALID_SERIES_DESCRIPTION,
        )
    yield client_with_user
    with persisting_db.connection_context():
        DataEventSeries.truncate_table()
