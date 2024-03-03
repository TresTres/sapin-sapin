import os
import typing 
from functools import wraps
from flask import Flask, Response, request
from flask_cors import CORS

from backend.db import db
from backend.server.migrations import migrate, create_test_user
from backend.server.logging import logger, configure_logging
from backend.server.blueprints import *
from backend.server.routes import register_routes


def create_app(mode: str) -> Flask:
    """
    Factory pattern to generate a Flask app
    """
    app = Flask(__name__)
    # TODO: Setup singular domain and disable CORS(?)
    CORS(app, supports_credentials=True)
    app.config.from_object(f"config.{mode.lower()}_config")
    app.register_blueprint(users_blueprint)
    app.register_blueprint(data_blueprint)

    configure_logging(app.config)
    
    # Prepare the database and set up routes
    db.init(app.config.get("DATABASE_URL", ":memory:"))
    migrate(db)
    if mode == "DEV":
        create_test_user(db)
    register_routes(app.config)

    logger.info(f"App mode: {mode}")
    logger.info(f"Pragmas: {db._pragmas}")
    logger.info(app.url_map)

    @app.before_request
    def _db_connect() -> None:
        logger.info(f"Request: {request}")
        logger.debug(f"Request Headers: {request.headers}")
        logger.debug(f"Request Data: {request.get_data()}")
        db.connect()

    @app.after_request
    def _see_response(response: Response) -> Response:
        logger.info(f"Response: {response}")
        logger.debug(f"Response Headers: {response.headers}")
        logger.debug(f"Response Data: {response.get_data()}")
        return response

    @app.teardown_request
    def _db_close(_exc) -> None:
        if not db.is_closed():
            db.close()

    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    @app.errorhandler(404)
    def not_found(_e: Exception) -> Response:
        return {"error": "Not found"}, 404

    return app



def jwt_authenticated(f: typing.Callable) -> typing.Callable:
    """
    Decorator to check if a user is authenticated using JWT by checking the Authorization header.
    The request object must be reachable.
    """

    @wraps(f)
    def decorated(*args, **kwargs) -> typing.Callable:
        token = request.headers.get("Authorization")
        if not token:
            abort(
                401,
                message="No token provided",
                headers={"WWW-Authenticate": "Basic realm='Valid login required'"},
            )
        try:
            payload = jwt.decode(
                token.split(" ")[1],
                key=current_app.config["ACCESS_KEY_SECRET"],
                algorithms=["HS256"],
            )
            user_id = payload["user"]
            # TODO: Implement a check against cookie for fingerprint once https is working
            # if payload["fingerprint"] != request.cookies.get("additional_token"):
            #     abort(401, message="Invalid token")
        except jwt.ExpiredSignatureError as ese:
            logger.error(f"Token has expired: {ese}")
            abort(401, message="Token has expired, re-login is required.")
        except jwt.InvalidTokenError as ite:
            logger.error(f"Invalid token: {ite}")
            abort(401, message="Invalid token")
        return f(*args, **kwargs, user_id=user_id)

    return decorated