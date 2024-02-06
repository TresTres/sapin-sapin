import peewee
import pytest

from backend.models import * 


MODELS = [User,]


@pytest.fixture(scope="module")
def db() -> peewee.SqliteDatabase:
    """Create a database connection with tables loaded"""
    db = peewee.SqliteDatabase(":memory:")
    with db.bind_ctx(MODELS):
        db.create_tables(MODELS, safe=True)
        with db.connection_context():
            yield db
        db.drop_tables(MODELS, safe=True)
        