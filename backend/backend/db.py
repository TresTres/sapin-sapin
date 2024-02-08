from peewee import SqliteDatabase

db = SqliteDatabase(None, pragmas={
    'journal_mode': 'wal',
    'foreign_keys': 1,
    'ignore_check_constraints': 0,
})
