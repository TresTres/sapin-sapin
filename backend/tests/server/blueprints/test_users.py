import werkzeug
import pytest
from unittest.mock import patch

from backend.server.routes import create_resource_path
from backend.models import User
from backend.db import db
from tests.constants import *


@pytest.fixture(scope="function")
def client_with_user(
    client: werkzeug.test.Client,
) -> typing.Generator[werkzeug.test.Client, None, None]:
    """
    Create a user for testing
    """
    with db.connection_context():
        User.create(
            username=VALID_USERNAME,
            email=VALID_EMAIL,
            password=VALID_PASSWORD,
            date_joined=VALID_JOIN_DATE,
        )
    yield client
    with db.connection_context():
        User.truncate_table()


class TestUserRegistration:

    @pytest.mark.parametrize(
        "username, email, password, expected_message",
        [
            ("", VALID_EMAIL, VALID_PASSWORD, "Username is invalid"),
            (VALID_USERNAME, "", VALID_PASSWORD, "Email is invalid"),
            (VALID_USERNAME, VALID_EMAIL, "", "Password is invalid"),
        ],
    )
    def test_registration_failure_invalid_input(
        self,
        client: werkzeug.test.Client,
        username: str,
        email: str,
        password: str,
        expected_message: str,
    ) -> None:
        """
        Test exception when creating a user with invalid input
        """
        response = client.post(
            create_resource_path(client.application.config, "registration"),
            json={
                "username": username,
                "email": email,
                "password": password,
            },
        )
        assert response.status_code == 400
        assert expected_message in response.json["message"]

    def test_registration_failure_user_exists(
        self, client_with_user: werkzeug.test.Client
    ) -> None:
        """
        Test exception when creating a user that already exists
        """
        response = client_with_user.post(
            create_resource_path(client_with_user.application.config, "registration"),
            json={
                "username": VALID_USERNAME,
                "email": VALID_EMAIL,
                "password": VALID_PASSWORD,
            },
        )
        assert response.status_code == 409
        assert "User already exists" in response.json["message"]

    def test_registration_success(self, client: werkzeug.test.Client) -> None:
        """
        Test successful user registration
        """
        response = client.post(
            create_resource_path(client.application.config, "registration"),
            json={
                "username": VALID_USERNAME,
                "email": VALID_EMAIL,
                "password": VALID_PASSWORD,
            },
        )
        assert response.status_code == 201
        assert "new_user" in response.json


class TestUserLogin:

    @pytest.mark.parametrize(
        "identifier",
        [
            VALID_USERNAME,
            VALID_EMAIL,
        ],
    )
    def test_login_failure_user_does_not_exist(
        self, client: werkzeug.test.Client, identifier: str
    ) -> None:
        """
        Test exception when logging in a user that does not exist
        """
        response = client.post(
            create_resource_path(client.application.config, "login"),
            json={"identifier": identifier, "password": VALID_PASSWORD},
        )
        assert response.status_code == 401
        assert "Could not find user" in response.json["message"]

    def test_login_failure_incorrect_password(
        self, client_with_user: werkzeug.test.Client
    ) -> None:
        """
        Test exception when logging in a user that is not active
        """
        response = client_with_user.post(
            create_resource_path(client_with_user.application.config, "login"),
            json={"identifier": VALID_USERNAME, "password": ""},
        )
        assert response.status_code == 401
        assert "Incorrect password" in response.json["message"]

    def test_login_success(self, client_with_user: werkzeug.test.Client) -> None:
        """
        Test successful user login, includes both refresh and access token 
        """
        with patch("werkzeug.wrappers.Response.set_cookie") as mock_set_cookie:
            response = client_with_user.post(
                create_resource_path(client_with_user.application.config, "login"),
                json={"identifier": VALID_USERNAME, "password": VALID_PASSWORD},
            )
            assert response.status_code == 200
            assert "user" in response.json
            assert "password" not in response.json["user"]
            assert "Authorization" in response.headers
            assert "Bearer" in response.headers["Authorization"]
            mock_set_cookie.assert_called_once_with(
                "refresh_token", mock_set_cookie.call_args[0][1], httponly=True, max_age=1800
            )
