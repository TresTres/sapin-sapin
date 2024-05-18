import jwt
import werkzeug

from tests.constants import *


class TestJWTAuthenticatedRoute:

    def test_jwt_authenticate_failure_with_missing_token(
        self, client_with_protected_route: werkzeug.test.Client
    ) -> None:
        """
        Test that a request to a protected route without a token fails
        """

        response = client_with_protected_route.post("/protected")
        assert response.status_code == 401
        assert response.json["message"] == "No token provided"

    def test_jwt_authenticate_failure_with_invalid_token(
        self, client_with_protected_route: werkzeug.test.Client
    ) -> None:
        """
        Test that a request to a protected route with an invalid token fails
        """

        token = "invalid_token"
        headers = {"Authorization": f"Bearer {token}"}
        response = client_with_protected_route.post("/protected", headers=headers)
        assert response.status_code == 401
        assert "Invalid token" in response.json["message"]

    def test_jwt_authenticate_failure_with_incorrectly_signed_token(
        self, client_with_protected_route: werkzeug.test.Client
    ) -> None:
        """
        Test that a request to a protected route with an invalid token fails
        """

        token = jwt.encode(
            {"user": VALID_USER_ID, "exp": datetime.datetime.now(datetime.UTC)},
            key="invalid_secret",
            algorithm="HS256",
            headers={"typ": "JWT"},
        )

        headers = {"Authorization": f"Bearer {token}"}
        response = client_with_protected_route.post("/protected", headers=headers)
        assert response.status_code == 401
        assert "Invalid token" in response.json["message"]

    def test_jwt_authenticated_with_expired_token(
        self, client_with_protected_route: werkzeug.test.Client
    ) -> None:
        """
        Test that a request to a protected route with an expired token fails
        """

        token = jwt.encode(
            {"user": VALID_USER_ID, "exp": datetime.datetime(1990, 1, 1)},
            key=client_with_protected_route.application.config["ACCESS_KEY_SECRET"],
            algorithm="HS256",
            headers={"typ": "JWT"},
        )

        headers = {"Authorization": f"Bearer {token}"}
        response = client_with_protected_route.post("/protected", headers=headers)
        assert response.status_code == 401
        assert "Token has expired" in response.json["message"]

    def test_jwt_authenticated_with_valid_token(
        self, client_with_protected_route: werkzeug.test.Client
    ) -> None:

        token = jwt.encode(
            {
                "user": VALID_USER_ID,
                "exp": datetime.datetime.now(datetime.UTC)
                + datetime.timedelta(minutes=15),
            },
            key=client_with_protected_route.application.config["ACCESS_KEY_SECRET"],
            algorithm="HS256",
            headers={"typ": "JWT"},
        )

        headers = {"Authorization": f"Bearer {token}"}
        response = client_with_protected_route.post("/protected", headers=headers)
        assert response.status_code == 200
        assert "success" in response.json
