from backend.server.logging import logger
from backend.db import sql_db
from backend.models import *



USER_MODELS = [
    User,
]


def create_tables() -> None:
    """
    Create tables if they do not yet exist.
    """
    with sql_db.connection_context():
        sql_db.create_tables(USER_MODELS, safe=True)
        logger.info(f"Available tables: {sql_db.get_tables()}")
        

def db_init() -> None:
    """
    Initialize the database. 
    
    Create tables if they do not yet exist.
    Fill in data if it does not yet exist. 
    Run migrations? 
    """
    create_tables()
    # run_migrations()
    # fill_data()
