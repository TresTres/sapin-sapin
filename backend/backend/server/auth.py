import jwt
import typing
import hashlib
import datetime
from functools import wraps

from flask import request, current_app, jsonify, Response

from backend.models import User
from backend.server.logging import logger


def generate_refresh_token(user: User, fingerprint: str) -> str:
    """
    Generate a JWT token with a 15 minute expiration period for an authenticated user
    """
    digest = hashlib.sha256(fingerprint.encode()).hexdigest()
    return jwt.encode(
        {
            "user": user.id,
            "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15),
            "fingerprint": digest,
        },
        key=current_app.config["REFRESH_KEY_SECRET"],
        algorithm="HS256",
        headers={"typ": "JWT"},
    )


def generate_access_token(user: User, fingerprint: str) -> str:
    """
    Generate a JWT token with a 1 minute expiration period for an authenticated user
    """
    digest = hashlib.sha256(fingerprint.encode()).hexdigest()
    return jwt.encode(
        {
            "user": user.id,
            "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=1),
            "fingerprint": digest,
        },
        key=current_app.config["ACCESS_KEY_SECRET"],
        algorithm="HS256",
        headers={"typ": "JWT"},
    )


def jwt_authenticated(f: typing.Callable) -> typing.Callable:
    """
    Decorator to check if a user is authenticated using an access token JWT by checking the Authorization header.
    """

    @wraps(f)
    def decorated(*args, **kwargs) -> Response:
        token = request.headers.get("Authorization").split(" ")[1]
        if not token:
            logger.error("No token provided")
            return (
                jsonify(
                    {
                        "message": "No token provided",
                        "headers": {
                            "WWW-Authenticate": "Basic realm='Valid login required'"
                        },
                    }
                ),
                401,
            )
        try:
            payload = jwt.decode(
                token,
                key=current_app.config["ACCESS_KEY_SECRET"],
                algorithms=["HS256"],
                options={
                    "verify_signature": True,
                    "verify_exp": True,
                },
            )
            user_id = payload["user"]
            # TODO: Implement a check against cookie for fingerprint once https is working
            # if payload["fingerprint"] != request.cookies.get("additional_token"):
            #     abort(401, message="Invalid token")
        except jwt.ExpiredSignatureError as ese:
            logger.error(f"Token has expired: {ese}")
            return jsonify({"message": "Token has expired, renewal is required."}), 401
        except jwt.InvalidTokenError as ite:
            logger.error(f"Invalid token: {ite}")
            return jsonify({"message": f"Invalid token, {ite}"}), 401
        return f(*args, **kwargs, user_id=user_id)

    return decorated
