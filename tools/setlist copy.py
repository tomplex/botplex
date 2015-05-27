__author__ = 'carusot'

import re
import requests


class Setlist(object):

    def __init__(self, date):
        r = requests.get('http://www.aqueousband.com/shows/{}.json'.format(date))
        if r.status_code == 200:
            self.raw = r.json()
            self.compiled = Setlist.full_output(self.raw)
        else:
            print('Input date does not match any setlist')


    def __getitem__(self, key):
        return self[key]

    def full_output(show_json):
        # produces the full string that the bot returns in a comment
        def prettify_date(show_json):
            sdate = show_json['performed_at'][:10]
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
                if num.startswith('0'):
                    num = num.lstrip('0')
                return num+suff

            date = monthdict[match[0][1]]+' '+suffix(match[0][2])+match[0][0]
            return date+'\n\n'
        # takes a YYYY-MM-DD date and makes it MONTH DAY, YEAR

        def find_loc(show_json):
            return show_json['venue']['name']+', '+show_json['venue']['location']+'\n\n'
            # finds the location/date info for this show

        def full_setlist(show_json):

            def comp_set(setIn):

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

                songs = ''
                song_list = [ str(det_cover(x['name'],x)+(det_tran(x))) for x in setIn['songs'] ]
                for x in song_list:
                    songs += x
                return songs.rstrip(', ')
            # compiles a setlist as a string

            sets = show_json['setlists']
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
                    snum = 'ENCORE:'
                    s = s+snum+' '+songs+'\n\n'
            else:
                for setlist in sets:
                    songs = comp_set(setlist)
                    s = s+snum.format(str(z))+' '+songs+'\n\n'

            return s


        def this_show(show_json):
            return '[[Full show notes and media]]({})'.format(show_json['url'])
        # returns the link to this show

        def other_shows(show_json):
            return '[[All shows at this venue]]({})'.format(show_json['venue']['url'])
        # returns the link to other shows at this venue


        return prettify_date(show_json)+find_loc(show_json)+full_setlist(show_json)+this_show(show_json)+'\n\n'+other_shows(show_json)

    def prettify_date(show_json):
            sdate = show_json['performed_at'][:10]
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
                if num.startswith('0'):
                    num = num.lstrip('0')
                return num+suff

            date = monthdict[match[0][1]]+' '+suffix(match[0][2])+match[0][0]
            return date
        # takes a YYYY-MM-DD date and makes it MONTH DAY, YEAR

    def find_loc(show_json):

        return show_json['venue']['name']+', '+show_json['venue']['location']
        # finds the location/date info for this show

    def full_setlist(show_json):

        def comp_set(setIn):

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

            songs = ''
            song_list = [ str(det_cover(x['name'],x)+(det_tran(x))) for x in setIn['songs'] ]
            for x in song_list:
                songs += x
            return songs.rstrip(', ')
        # compiles a setlist as a string

        sets = show_json['setlists']
        snum = 'SET {}:'
        z = 1
        s = ''
        if len(sets) > 1:
            for setlist in sets[0:-1]:
                songs = comp_set(setlist)
                s = s+snum.format(str(z))+' '+songs
                z = z+1
            for setlist in sets[-1:]:
                songs = comp_set(setlist)
                snum = 'ENCORE:'
                s = s+snum+' '+songs
        else:
            for setlist in sets:
                songs = comp_set(setlist)
                s = s+snum.format(str(z))+' '+songs

        return s

    def this_show(show_json):
        return '[[Full show notes and media]]({})'.format(show_json['url'])

    def other_shows(show_json):
        return '[[All shows at this venue]]({})'.format(show_json['venue']['url'])

    def comp_set(setIn):

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

            songs = ''
            song_list = [ str(det_cover(x['name'],x)+(det_tran(x))) for x in setIn['songs'] ]
            for x in song_list:
                songs += x
            return songs.rstrip(', ')
        # compiles a setlist as a string

