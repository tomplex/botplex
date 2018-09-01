
__author__ = 'tom caruso'

import yaml
import logging

import setlist

from bot import Bot
from archive_manager import run_full_metadata_update, run_partial_metadata_update

SUBREDDIT = 'aqueousband'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

with open('settings.yml') as f:
    settings = yaml.load(f)


def main():
    logging.info("Starting up.")
    # bot = Bot(settings)
    # for cmt in bot.fetch_comments(SUBREDDIT, key=setlist.has_setlist_mark):
    #     pass
    run_full_metadata_update()



if __name__ == '__main__':
    main()
