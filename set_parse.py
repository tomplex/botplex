__author__ = 'carusot'

import re

def det_tran(son):
    if son['transition'] == True:
        return '> '
    else:
        return ', '
# determines if a song has a transition

def det_cover(son,thisSong):
    if thisSong['cover'] == True:
        return r"*"+son+r"*"
    else:
        return son
# determines if a song is a cover

def find_notes(son):
    song_notes = str([x for x in son['notes']])
    return song_notes.strip('[').strip(']')
# finds song notes; unused

def comp_set(setIn):
    s = ''
    ind = 0
    song_list = [ str(det_cover(str(x['name']),x)+(str(det_tran(x)))) for x in setIn['songs'] ]
    for x in song_list:
        s = s+r'{}'.format(song_list[ind])
        ind = ind+1
    return s.rstrip(', ')
# compiles a setlist as a string

def prettify_date(showIn):
    sdate = showIn['performed_at'][:10]
    pattern = r'(\d\d\d\d)-(\d\d)-(\d\d)'
    match = re.findall(pattern, sdate)
    monthdict = {'01':'January', '02':'February','03':'March','04':'April','05':'May','06':'June','07':'July',
                 '08':'August','09':'September','10':'October','11':'November','12':'December'}

    def suffix(num):
        if num[1] == '1':
            suff = 'st, '
        elif num[1] == '2':
            suff = 'nd, '
        elif num[1] == '3':
            suff = 'rd, '
        else:
            suff = 'th, '
        return num+suff

    date = monthdict[match[1]]+' '+suffix(match[2])+match[0]
    return date

def find_loc(showIn):
    return prettify_date(showIn)+'\n\n'+showIn['venue']['name']+', '+showIn['venue']['location']+'\n\n'
# finds the location/date info for this show

def this_show(showIn):
    return '[[Full show notes and media]]({})'.format(showIn['url'])+ '\n\n'
# returns the link to this show

def other_shows(showIn):
    return '[[All shows at this venue]]({})'.format(showIn['venue']['url'])
# returns the link to other shows at this venue

def full_setlist(showIn):
    sets = showIn['setlists']
    snum = 'SET {}:'
    z = 1
    s = ''
    if len(sets) > 1:
        for setlist in sets[0:-1]:
            songs = comp_set(setlist)
            s = s+snum.format(str(z))+' '+songs+'\n\n'
            z = z+1
        for setlist in sets[-1:]:
            songs = comp_set(setlist)
            snum = 'ENCORE :'
            s = s+snum+' '+songs+'\n\n'
    else:
        for setlist in sets:
            songs = comp_set(setlist)
            s = s+snum.format(str(z))+' '+songs+'\n\n'

    return s
# adds SET 1, SET 2, etc and compiles all the sets of the shows into one string

def full_output(showIn):
    return find_loc(showIn)+full_setlist(showIn)+this_show(showIn)+other_shows(showIn)
# produces the full string that the bot returns in a comment

def checker(body):
    pattern = r'AQ(\d\d\d\d-\d\d-\d\d)'
    match = re.findall(pattern, body)
    if match:
        return match[0]
    else:
        return None

# checks to see if the extracted value is a date