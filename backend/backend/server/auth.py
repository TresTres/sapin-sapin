import jwt
import typing 
from functools import wraps

from flask import request, current_app, jsonify, Response
from backend.server.logging import logger


def jwt_authenticated(f: typing.Callable) -> typing.Callable:
    """
    Decorator to check if a user is authenticated using JWT by checking the Authorization header.
    The request object must be reachable.
    """

    @wraps(f)
    def decorated(*args, **kwargs) -> Response:
        token = request.headers.get("Authorization")
        if not token:
            logger.error("No token provided")
            return jsonify(
                {
                    "message": "No token provided",
                    "headers": {"WWW-Authenticate": "Basic realm='Valid login required'"},
                }
            ), 401
        try:
            payload = jwt.decode(
                token.split(" ")[1],
                key=current_app.config["ACCESS_KEY_SECRET"],
                algorithms=["HS256"],
                options={
                    'verify_signature': True,
                    'verify_exp': True,
                }
            )
            user_id = payload["user"]
            # TODO: Implement a check against cookie for fingerprint once https is working
            # if payload["fingerprint"] != request.cookies.get("additional_token"):
            #     abort(401, message="Invalid token")
        except jwt.ExpiredSignatureError as ese:
            logger.error(f"Token has expired: {ese}")
            return jsonify({"message": "Token has expired, re-login is required."}), 401
        except jwt.InvalidTokenError as ite:
            logger.error(f"Invalid token: {ite}")
            return jsonify({"message": f"Invalid token, {ite}"}), 401
        return f(*args, **kwargs, user_id=user_id)

    return decorated