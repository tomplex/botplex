
__author__ = 'tom caruso'

import praw
import setlist

from datetime import datetime
from collections import namedtuple

submission = namedtuple('submission', ['id', 'body', 'author', 'post_date', 'request_date'])
comment = namedtuple('comment', ['id', 'body', 'author', 'post_date', 'request_date'])


class Bot:
    def __init__(self, settings):
        self._settings = settings
        self._praw = self.login()

    def login(self):
        return praw.Reddit(client_id=self._settings['client_id'],
                           client_secret=self._settings['client_secret'],
                           username=self._settings['username'],
                           password=self._settings['password'],
                           user_agent=self._settings['user_agent']
                           )

    def fetch_comments(self, subreddit, key=None):
        if not key:
            key = lambda x: x
        for cmt in filter(key, self._praw.subreddit(subreddit).comments()):
            yield cmt

    def fetch_submissions(self, subreddit, key=None):
        if not key:
            key = lambda x: x
        for sbm in filter(key, self._praw.subreddit(subreddit).submissions()):
            yield sbm

    def get_comment(self, cmt_id):
        return self._praw.comment(cmt_id)

    def get_submission(self, sub_id):
        return self._praw.submission(sub_id)

    def reply(self, item, message):
        pass
