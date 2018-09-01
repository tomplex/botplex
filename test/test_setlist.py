import json

from setlist import generate_setlist_markdown

__author__ = 'tom caruso'

import pytest

processed = \
"""##The Rex Theater Pittsburgh, PA - 2017-12-16
---
#####Set One

*For Whom the Bell Tolls* ^1 > Kitty Chaser (Explosions) ^2, Aldehyde > Random Company, Gordon's Mule

#####Set Two

20/20, Numbers and Facts, Triangle

#####Encore

*A Day in the Life*

##### Notes

1: Intro only

2: The Imperial March (John Williams) teases

---

[This setlist on aqueousband.com](https://aqueousband.com/shows/2017-12-16)

[Listen on archive.org](https://archive.org/details/aqueous2017-12-16.CM33)

[Listen on nugs.net](http://nugs.net/live-music/0,18732/Aqueous-mp3-flac-download-12-16-2017-The-Rex-Theater-Pittsburgh-PA.html)

Problems? Contact /u/eyesoftheworld"""


@pytest.fixture()
def show_json():
    with open('/Users/tom/dev/botplex/test/setlist_data.json') as f:
        yield json.load(f)


def test_generate_setlist_markdown(show_json):
    md = generate_setlist_markdown(show_json)
    print(md)
    assert md == processed
