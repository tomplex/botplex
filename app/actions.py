import logging
import time

from praw import exceptions
from datetime import datetime

from app.database import Database
from app.reddit_bot import RedditBot
from app import setlist

SUBREDDIT = 'aqueousband'


def less_than_a_week_old(timestamp: int) -> bool:
    d1 = datetime.fromtimestamp(timestamp)
    d2 = datetime.now()

    return (d2 - d1).days <= 7


def should_respond(created, text, author) -> bool:
    return less_than_a_week_old(created) and setlist.has_setlist_mark(text) and author != 'botplex'


def reddit_bot_loop():
    logging.info("Starting reddit bot loop")
    bot = RedditBot()
    db = Database()

    while db.any_update_in_progress():
        # If any metadata updates are happening, wait for them to finish.
        logging.info("Waiting for updates to finish...")
        time.sleep(10)

    for comment in bot.fetch_comments(SUBREDDIT, key=lambda cmt: not db.replied_to_comment(cmt.id) and should_respond(cmt.created, cmt.body, cmt.author)):
        logging.info("Responding to comment: " + str(comment))

        for requested_date in setlist.get_setlist_dates(comment.body):
            reply_text = setlist.get_setlist(requested_date)
            try:
                comment.reply(reply_text)
                db.record_comment_reply(comment, requested_date)
            except exceptions.APIException as e:
                # Probably a RateLimit
                logging.info("caught an exception: " + str(e))
                logging.info("sleeping..")
                time.sleep(5)

    for submission in bot.fetch_submissions(SUBREDDIT, key=lambda sub: not db.replied_to_comment(sub.id) and should_respond(sub.created, sub.selftext, sub.author)):
        logging.info("Responding to submission: " + str(submission))

        for requested_date in setlist.get_setlist_dates(submission.selftext):
            reply_text = setlist.get_setlist(requested_date)
            try:
                submission.reply(reply_text)
                db.record_submission_reply(submission, requested_date)
            except exceptions.APIException as e:
                # Probably a RateLimit
                logging.info("caught an exception: " + str(e))
                logging.info("sleeping..")
                time.sleep(5)

    logging.info("Complete.")
    db.connection.close()
