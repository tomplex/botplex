__author__ = 'carusot'

import time
import json

import praw
import requests

from set_parse import full_output, checker


checkList = r'/Users/carusot/Documents/Python/setlistBot/aq/checked'
#checkList = r'/home/tomplex/botplex/checked'

# loads list of comments that have been replied to already
with open(checkList, 'r') as f:
    checked = json.load(f)


# bot itself
bot = praw.Reddit('Aqueous setlist fetcher, v1.1 by /u/eyesoftheworld4')
bot.login('botplex','warren')

# forever:
while True:
    # get comments for
    sub = bot.get_subreddit('aqueousband')
    cmts = sub.get_comments()

    for comment in cmts:
        body = comment.body
        if 'AQ' in body and comment.id not in checked:
            checked.append(comment.id)
            with open(checkList, 'w') as f:
                json.dump(checked, f)

            if checker(body) is None:
                continue

            r = requests.get('http://aqueousband.com/shows/{}.json'.format(checker(body)))

            if r.status_code == 200:
                comment.reply(full_output(r.json()))
                print('replied with setlist')
                time.sleep(300)


            else:
                comment.reply('Sorry, setlist not found. Check to see if you have [the right date.]'
                              '(http://www.aqueousband.com/shows)')
                print('replied with setlist not found')
                time.sleep(300)


        else:
            pass
    x = time.localtime()
    print(str(x[0])+'-'+str(x[1])+'-'+str(x[2])+', '+str(x[3])+'hrs '+str(x[4])+'mins '+str(x[5])+'sec'+
          ':sleeping for 10 minutes')
    time.sleep(600)












