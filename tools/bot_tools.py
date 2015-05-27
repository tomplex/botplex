__author__ = 'carusot'

import re
import requests
import json

import praw
import time

checkList = r'/home/tomplex/botplex/checked'
logp = '/home/tomplex/botplex/log'
#checkList = r'/Users/carusot/Documents/Python/setlistBot/aq/checked'
#logp = '/Users/carusot/Documents/Python/setlistBot/aq/log'

with open(checkList, 'r') as f:
    checked = json.load(f)



def stamp(In):
    x = time.localtime()
    if In ==  'date':
        out = str(x[0])+'-'+str(x[1])+'-'+str(x[2])+', '
    elif In == 'time':
        hr = str(x[3])
        mins = str(x[4])
        sec = str(x[5])
        if not len(hr) == 2:
            hr = '0'+hr
        if not len(mins) == 2:
            mins = '0'+mins
        if not len(sec) == 2:
            sec = '0'+sec
        out = hr+':'+mins+':'+sec+' - '
    else:
        out = None
    return out
# returns time or date stamp used in the log

def checker(body, id):
    if 'AQ' in body and id not in checked:
        checked.append(id)
        with open(checkList, 'w') as a:
            json.dump(checked, a)
        return True
    else:
        return False
# checks to see if the comment has been replied to already

def find_date(text):
    pattern = r'AQ(\d\d\d\d-\d\d-\d\d)'
    match = re.findall(pattern, text)
    if match:
        return match[0]
    else:
        return '0000-00-00'


def log(text):
    with open(logp, 'a') as l:
        l.write(stamp('date')+stamp('time')+text+'\n')


def reply(postxt, comment, num):
    logtxt = {0:'Replied with setlist', 3:'Reddit error, waiting 5 minutes',
              2:'Unresolvable reddit error, ignoring comment', 1:'Replied with setlist not found'}
    try:
        praw.objects.Comment.reply(comment, postxt)
        log(logtxt[num])
        time.sleep(300)

    except requests.HTTPError:
        log(logtxt[3])
        time.sleep(300)
        try:
            praw.objects.Comment.reply(comment, postxt)
            log(logtxt[num])
            time.sleep(300)
        except requests.HTTPError:
            log(logtxt[2])
            time.sleep(600)
    return None
