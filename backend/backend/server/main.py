
from flask import Flask, Response

from backend.db import sql_db as db
from backend.server.initialization import db_init
from backend.server.logging import logger
from backend.server.blueprints import *

def create_app() -> Flask:
    """
    App factory pattern
    """
    app = Flask(__name__)
    db_init()
    app.register_blueprint(users_blueprint)

    logger.info(f"Pragmas: {db._pragmas}")

    @app.before_request
    def _db_connect() -> None:
        db.connect()

    @app.teardown_request
    def _db_close(response: Response) -> Response:
        if not db.is_closed():
            db.close()
        return response
            

    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    return app

