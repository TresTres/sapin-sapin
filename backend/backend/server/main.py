import logging
from logging.handlers import RotatingFileHandler
from flask import Flask

from backend.db.management import sql_db as db
from backend.models import *

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a handler for stdout
stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.INFO)
logger.addHandler(stdout_handler)

# Create a handler for the log file
file_handler = RotatingFileHandler('logs/server.log', maxBytes=1024, backupCount=3)
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)



def create_app() -> Flask:
    app = Flask(__name__)

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

