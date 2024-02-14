import pytest
import peewee
import typing

from backend.db import PRAGMAS
from backend.server.migrations import MODELS


@pytest.fixture(scope="class", autouse=True)
def db() -> typing.Generator[peewee.SqliteDatabase, None, None]:
    """Create a database connection with tables loaded"""
    db = peewee.SqliteDatabase(":memory:", pragmas=PRAGMAS)
    with db.bind_ctx(MODELS):
        db.create_tables(MODELS, safe=True)
        with db.connection_context():
            yield db
        db.drop_tables(MODELS, safe=True)
