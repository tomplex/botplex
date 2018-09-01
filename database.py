import sqlite3
import os

from pathlib import Path

PRODUCTION_DATABASE_NAME = str(Path(__file__).parent / 'botplex.sqlite')
TEST_DATABASE_NAME = str(Path(__file__).parent / 'test.sqlite')

database_name = TEST_DATABASE_NAME
if os.environ.get('BOTPLEX_ENVIRONMENT', '') == 'production':
    database_name = PRODUCTION_DATABASE_NAME


class Database:
    def __init__(self, name=database_name):
        self._conn = sqlite3.connect(name)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        for row in self.cursor:
            yield row

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def record_comment_reply(self, cmt):
        # yield comment(id=cmt.id,
        #            body=cmt.body,
        #            author=cmt.author,
        #            post_date=datetime.fromtimestamp(cmt.created),
        #            request_date=setlist.get_setlist_dates(cmt.body))
        pass

    def record_submission_reply(self, subm):
        # yield submission(id=sbm.id,
        #            body=sbm.selftext,
        #            author=sbm.author,
        #            post_date=datetime.fromtimestamp(sbm.created),
        #            request_date=setlist.get_setlist_dates(sbm.selftext))
        pass

    def replied_to_comment(self, cmt):
        pass
