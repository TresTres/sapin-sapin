import os
import json
from flask import Flask, Response, request
from flask_cors import CORS

from backend.db import db
from backend.server.migrations import migrate, create_test_user
from backend.server.logging import logger, configure_logging
from backend.server.blueprints import *
from backend.server.routes import register_routes
from backend.server.blueprints.utils import camel_case_payload


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
    os.makedirs("sqlite", exist_ok=True)
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
    def _convert_payload(response: Response) -> Response:
        # TODO: If you have to change this, switch to creating a custom response class
        if response.is_json:
            response.data = json.dumps(
                camel_case_payload(response.get_json())
            )
        return response

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
