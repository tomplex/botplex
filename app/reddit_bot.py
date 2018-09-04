__author__ = 'tom caruso'


import os
import praw


class RedditBot:
    def __init__(self):
        self._praw = None
        self.login()

    def login(self):
        self._praw = praw.Reddit(client_id=os.environ['BOTPLEX_CLIENT_ID'],
                           client_secret=os.environ['BOTPLEX_CLIENT_SECRET'],
                           username=os.environ['BOTPLEX_USERNAME'],
                           password=os.environ['BOTPLEX_PASSWORD'],
                           user_agent=os.environ['BOTPLEX_USER_AGENT']
                           )

    def fetch_comments(self, subreddit, key=None):
        if not key:
            key = lambda x: x
        for cmt in filter(key, self._praw.subreddit(subreddit).comments()):
            yield cmt

    def fetch_submissions(self, subreddit, key=None):
        if not key:
            key = lambda x: x
        for sbm in filter(key, self._praw.subreddit(subreddit).new()):
            yield sbm

    def get_comment(self, cmt_id):
        return self._praw.comment(cmt_id)

    def get_submission(self, sub_id):
        return self._praw.submission(sub_id)

    def reply(self, item, message):
        item.reply(message)
