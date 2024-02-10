import pytest
import peewee

from backend.server.migrations import MODELS


@pytest.fixture(scope="class", autouse=True)
def db() -> peewee.SqliteDatabase:
    """Create a database connection with tables loaded"""
    db = peewee.SqliteDatabase(":memory:")
    with db.bind_ctx(MODELS):
        db.create_tables(MODELS, safe=True)
        with db.connection_context():
            yield db
        db.drop_tables(MODELS, safe=True)
