import os
from flask import Flask, Response, Config, request
from flask_cors import CORS

from backend.db import db
from backend.server.migrations import migrate
from backend.server.logging import logger, configure_logging
from backend.server.blueprints import *
from backend.server.routes import register_routes


def prepare_db(app_config: Config) -> None:
    """
    Prepare the database
    """
    db.init(app_config.get("DATABASE_URL", ":memory:"))
    migrate(db)


def create_app(mode: str) -> Flask:
    """
    Factory pattern to generate a Flask app
    """
    app = Flask(__name__)
    # CORS(app)
    app.config.from_object(f"config.{mode.lower()}_config")
    app.register_blueprint(users_blueprint)

    configure_logging(app.config)
    prepare_db(app.config)
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
