from flask import Flask, Response
from flask_cors import CORS

from backend.db import sql_db as db
from backend.server.initialization import db_init
from backend.server.logging import logger
from backend.server.blueprints import *



def create_app() -> Flask:
    """
    App factory pattern
    """
    app = Flask(__name__)
    CORS(app)
    db_init()
    app.register_blueprint(users_blueprint)

    logger.info(f"Pragmas: {db._pragmas}")

    @app.before_request
    def _db_connect() -> None:
        db.connect()
        
    @app.after_request
    def _see_response(response: Response) -> Response:
        logger.debug(f"Response: {response.get_data()}")
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

