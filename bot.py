__author__ = 'carusot'

import time
import praw


from aq.tools.setlist import Setlist

from aq.tools.bot_tools import reply,log,checker,find_date


# bot itself
bot = praw.Reddit('Aqueous setlist fetcher, v1.2 by /u/eyesoftheworld4')
bot.login('botplex', 'warren')

while True:

    sub = bot.get_subreddit('aqueousband')

    for comment in sub.get_comments():

        if checker(comment.body, comment.id) is False:
            continue


        set = Setlist(find_date(comment.body))

        if set.compiled is None:
            reply('Sorry, setlist not found!', comment, 1)

        else:
            reply(set.compiled, comment, 0)



    log('waiting 10 minutes to re-check comments')
    time.sleep(600)












