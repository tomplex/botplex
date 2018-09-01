
__author__ = 'tom caruso'


import re
import requests
import typing

import archive_manager
import nugs_manager


AQ_SHOW_DATE = re.compile('AQ(\d\d\d\d-\d\d-\d\d)|AQ(\d\d\d\d\d\d\d\d)')


def has_setlist_mark(body: str):
    if AQ_SHOW_DATE.search(body):
        return True
    return False


def get_setlist_dates(comment: str):
    return AQ_SHOW_DATE.findall(comment)


def get_setlist(date: str) -> str:
    data = get_show_data(date)
    if not data:
        return ''
    return generate_setlist_markdown(data)


def get_show_data(date: str) -> dict:
    resp = requests.get(f'http://aqueousband.com/shows/{date}.json')
    if resp.ok:
        return resp.json()
    return {}


def process_song(song: dict, last_song: bool, note_counter: int) -> typing.Tuple[str, dict]:
    processed = song['name']
    notes = {}
    if song['cover']:
        processed = '*' + processed + '*'
    if song['notes']:
        for note in song['notes']:
            processed += f' ^{note_counter}'
            notes[note_counter] = note
            note_counter += 1
    if song['transition']:
        processed += ' > '
    elif not last_song:
        processed += ', '
    return processed, notes


def generate_setlist_markdown(show_data: dict) -> str:
    note_counter = 1
    all_notes = {}
    markdown = f"""##{show_data['venue']['name']} {show_data['venue']['location']} - {show_data['performed_at']}\n---\n"""
    for setlist in show_data['setlists']:
        markdown += f"""#####{setlist['name'].title()}\n\n"""

        for idx, song in enumerate(setlist['songs']):
            last_song = idx == len(setlist['songs']) - 1
            processed, song_notes = process_song(song, last_song, note_counter)
            all_notes = {**all_notes, **song_notes}
            note_counter += len(song_notes)
            markdown += processed

        markdown += """\n\n"""

    if all_notes:
        markdown += f"""##### Notes\n\n"""
        for counter, note in all_notes.items():
            markdown += f"""{counter}: {note}\n\n"""


    markdown += "---\n\n"
    markdown += f"[This setlist on aqueousband.com]({show_data['url']})\n\n"

    # Check for archive show or nugs show here
    archive_url =  archive_manager.archive_recording(show_data['performed_at'])
    if archive_url:
        markdown += f"[Listen on archive.org]({archive_url})\n\n"

    nugs_url = nugs_manager.nugs_recording_url(show_data['performed_at'])
    if nugs_url:
        markdown += f"[Listen on nugs.net]({nugs_url})\n\n"

    markdown += "Problems? Contact /u/eyesoftheworld"

    return markdown
