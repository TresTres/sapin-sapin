from peewee import SqliteDatabase

PRAGMAS = {
    "journal_mode": "wal",
    "foreign_keys": 1,
    "ignore_check_constraints": 0,
}

db = SqliteDatabase(
    None,
    pragmas=PRAGMAS,
)
