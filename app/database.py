import logging
import sqlite3
import os

from datetime import datetime

from app import basedir

env = os.environ.get('FLASK_ENV', '')

PRODUCTION_DATABASE_NAME = str(basedir / (env + '.sqlite'))
TEST_DATABASE_NAME = str(basedir / 'test.sqlite')

database_name = TEST_DATABASE_NAME

if env == 'production':
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

    def query(self, sql, params=None, return_all=False):
        self.cursor.execute(sql, params or ())
        if return_all:
            return self.fetchall()
        return self.fetchone() or ()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def record_comment_reply(self, cmt, request_date):
        self.execute("""
            INSERT INTO replies (id, author, post_date, request_date, reply_type, reply_date)
            VALUES 
                                (?, ?, ?, ?, 'comment', current_timestamp)
        """, (cmt.id, str(cmt.author), str(datetime.fromtimestamp(cmt.created)), str(request_date)))
        self.commit()

    def record_submission_reply(self, sub, request_date):
        self.execute("""
            INSERT INTO replies (id, author, post_date, request_date, reply_type, reply_date)
            VALUES 
                                (?, ?, ?, ?, 'submission', current_timestamp)
        """, (sub.id, str(sub.author), str(datetime.fromtimestamp(sub.created)), str(request_date)))
        self.commit()

    def replied_to_comment(self, cmt_id):
        return self.query('SELECT * FROM replies WHERE id = ?', (cmt_id,))
