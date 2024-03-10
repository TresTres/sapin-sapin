import datetime
from peewee import SqliteDatabase

from backend.server.logging import logger
from backend.models import *


USER_MODELS = [
    User,
]

DATA_MODELS = [
    DataEventSeries,
    DataEvent,
    DataRecurrence,
]

MODELS = [*USER_MODELS, *DATA_MODELS]


def create_tables(db: SqliteDatabase) -> None:
    """
    Create tables if they do not yet exist.
    """
    with db.connection_context():
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


def create_test_user(db: SqliteDatabase) -> None:
    """
    Create a test user if it does not yet exist.
    """
    with db.connection_context():
        try:
            _user, created = User.get_or_create(
                username="testuser1",
                email="foobar@baz.net",
                defaults={
                    "is_active": True,
                    "date_joined": datetime.datetime.now(datetime.UTC),
                    "password": "testPassword987%",
                },
            )
            if created:
                logger.info(f"Created test user")

        except IntegrityError:
            logger.warn("Test user already exists.  Skipping...")
