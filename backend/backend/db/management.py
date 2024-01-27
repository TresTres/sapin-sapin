from peewee import SqliteDatabase



sql_db = SqliteDatabase('core.db', pragmas={
    'journal_mode': 'wal',
    'foreign_keys': 1,
    'ignore_check_constraints': 0,
})