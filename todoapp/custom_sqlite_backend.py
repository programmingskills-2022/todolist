from django.db.backends.sqlite3.base import DatabaseWrapper as Sqlite3DatabaseWrapper

class CustomSqlite3DatabaseWrapper(Sqlite3DatabaseWrapper):
    def __init__(self, *args, **kwargs):
        kwargs['version'] = '3.8.3'
        super().__init__(*args, **kwargs)