import logging
from datetime import datetime, timedelta

from app.database import Database
from app.reddit_bot import RedditBot
from app import setlist

SUBREDDIT = 'testingground4bots'


def less_than_a_week_old(timestamp: int) -> bool:
    d1 = datetime.fromtimestamp(timestamp)
    d2 = datetime.now()
    monday1 = (d1 - timedelta(days=d1.weekday()))
    monday2 = (d2 - timedelta(days=d2.weekday()))

    weeks = (monday2 - monday1).days / 7
    return weeks == 0


def should_respond(created, text) -> bool:
    return less_than_a_week_old(created) and setlist.has_setlist_mark(text)


def reddit_bot_loop():
    logging.info("Starting reddit bot loop")
    bot = RedditBot()
    db = Database()

    for comment in bot.fetch_comments(SUBREDDIT, key=lambda cmt: not db.replied_to_comment(cmt.id) and should_respond(cmt.created, cmt.body)):
        logging.info("Responding to comment: " + str(comment))

        for requested_date in setlist.get_setlist_dates(comment.body):
            reply_text = setlist.get_setlist(requested_date)
            comment.reply(reply_text)
            db.record_comment_reply(comment, requested_date)

    for submission in bot.fetch_submissions(SUBREDDIT, key=lambda sub: not db.replied_to_comment(sub.id) and should_respond(sub.created, sub.selftext)):
        logging.info("Responding to submission: " + str(submission))

        for requested_date in setlist.get_setlist_dates(submission.selftext):
            reply_text = setlist.get_setlist(requested_date)
            submission.reply(reply_text)
            db.record_submission_reply(submission, requested_date)

    db.connection.close()
