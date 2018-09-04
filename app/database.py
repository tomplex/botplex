import psycopg2
import os

from datetime import datetime


def get_dsn():
    return f"host={os.environ.get('PGHOST')} port={os.environ.get('PGPORT')} user={os.environ.get('PGUSER')} password={os.environ.get('PGPASSWORD')}"


class Database:
    def __init__(self):
        self._conn = psycopg2.connect(get_dsn())
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
                                (%s, %s, %s, %s, 'comment', now())
        """, (cmt.id, str(cmt.author), str(datetime.fromtimestamp(cmt.created)), str(request_date)))
        self.commit()

    def record_submission_reply(self, sub, request_date):
        self.execute("""
            INSERT INTO replies (id, author, post_date, request_date, reply_type, reply_date)
            VALUES 
                                (%s, %s, %s, %s, 'submission', now())
        """, (sub.id, str(sub.author), str(datetime.fromtimestamp(sub.created)), str(request_date)))
        self.commit()

    def replied_to_comment(self, cmt_id):
        return self.query('SELECT * FROM replies WHERE id = %s', (cmt_id,))

    def any_update_in_progress(self):
        archive = self.query("SELECT refresh_in_progress FROM archive_metadata")
        nugs = self.query("SELECT refresh_in_progress FROM nugs_metadata")
        return archive[0] or nugs[0]
