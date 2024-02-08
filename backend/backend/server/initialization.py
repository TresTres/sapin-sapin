from peewee import SqliteDatabase

from backend.server.logging import logger
from backend.models import *


USER_MODELS = [
    User,
]


def create_tables(db: SqliteDatabase) -> None:
    """
    Create tables if they do not yet exist.
    """
    with db.connection_context():
        db.create_tables(USER_MODELS, safe=True)
        logger.info(f"Available tables: {db.get_tables()}")


def init_db(db: SqliteDatabase) -> None:
    """
    Initialize the database.

    Create tables if they do not yet exist.
    Fill in data if it does not yet exist.
    Run migrations?
    """
    create_tables(db)
    # run_migrations()
    # fill_data()
