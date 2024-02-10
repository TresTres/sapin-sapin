from peewee import SqliteDatabase

from backend.server.logging import logger
from backend.models import *


USER_MODELS = [
    User,
]

MODELS = USER_MODELS


@db.connection_context()
def create_tables(db: SqliteDatabase) -> None:
    """
    Create tables if they do not yet exist.
    """
    db.create_tables(MODELS, safe=True)
    logger.info(f"Available tables: {db.get_tables()}")


def migrate(db: SqliteDatabase) -> None:
    """
    Initialize the database.

    Create tables if they do not yet exist.
    Fill in data if it does not yet exist.
    Run migrations?
    """
    create_tables(db)
    # fill_data()
