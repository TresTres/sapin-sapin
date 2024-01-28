import os
from peewee import SqliteDatabase


DATABASE_URL = os.environ.get('DATABASE_URL', '/app/sqlite/core.db')

sql_db = SqliteDatabase(DATABASE_URL, pragmas={
    'journal_mode': 'wal',
    'foreign_keys': 1,
    'ignore_check_constraints': 0,
})
