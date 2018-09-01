import pytest

from archive_manager import get_date_query, link_from_wikilink


@pytest.mark.parametrize('_from,_to,expected', [
    ('2018-01-01', None, '[2018-01-01 TO null]'),
    (None, None, '[null TO null]'),
    ('2018-01-01', '2018-05-01', '[2018-01-01 TO 2018-05-01]'),
    (None, '2018-04-06', '[null TO 2018-04-06]')
])
def test_get_date_query(_from, _to, expected):
    assert get_date_query(_from, _to) == expected


@pytest.mark.parametrize('wikilink,expected', [
    ("* [https://archive.org/details/AQ2012-10-18.boardmultitrack AQ2012-10-18.boardmultitrack] -- Aqueous Live at Java Barn on 2012-10-18", 'https://archive.org/details/AQ2012-10-18.boardmultitrack'),
    ("* [https://archive.org/details/AQ2012-11-03.AQ2012-11-03 AQ2012-11-03.AQ2012-11-03] -- Aqueous Live at Nietzsche's on 2012-11-03", 'https://archive.org/details/AQ2012-11-03.AQ2012-11-03'),
    ("* [https://archive.org/details/AQ2013-03-21.flac24 AQ2013-03-21.flac24] -- Aqueous Live at The Club at Water Street on 2013-03-21", 'https://archive.org/details/AQ2013-03-21.flac24')
])
def test_get_link_from_wikilink(wikilink, expected):
    assert link_from_wikilink(wikilink) == expected