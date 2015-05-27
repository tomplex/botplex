__author__ = 'carusot'

from aq.tools.setlist import Setlist
import requests as r

s = r.get('http://www.aqueousband.com/shows/2014-04-17.json')

show = Setlist(s.json())

print(show.date+'\n---------\n')
print(show.compiled+'\n---------\n')
print(show.loc+'\n-----------\n')
print(show.setlist+'\n-----------\n')