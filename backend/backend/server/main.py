
from flask import Flask

from backend.db import sql_db as db
from backend.server.initialization import db_init
from backend.server.logging import logger

def create_app() -> Flask:
    """
    App factory pattern
    """
    app = Flask(__name__)
    db_init()

    logger.info(f"Pragmas: {db._pragmas}")

    @app.before_request
    def _db_connect() -> None:
        db.connect()

    @app.teardown_request
    def _db_close(exc: Exception) -> None:
        if not db.is_closed():
            db.close()

    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    @app.post("/user")
    def create_user():
        pass

    return app

