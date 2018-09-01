import logging

from internetarchive import search_items
from database import Database


def run_full_metadata_update():
    logging.info("Running full Archive metadata update")
    with Database() as db:
        db.execute('DELETE FROM archive_items')
        db.cursor.executemany('INSERT INTO archive_items (aid, date_text, url) VALUES (?, ?, ?)', generate_all_items())
        db.execute('UPDATE archive_metadata SET last_full_refresh_date = current_date')

    logging.info("Update complete.")


def run_partial_metadata_update():
    logging.info("Running partial Archive metadata update")
    with Database() as db:
        last_partial_refresh = str(next(db.query('SELECT last_partial_refresh_date FROM archive_metadata'))[0])
        logging.info(f"Looking for shows added since last update at {last_partial_refresh}")

        db.cursor.executemany('INSERT INTO archive_items (aid, date_text, url) VALUES (?, ?, ?)', generate_added_items_in_date_range(last_partial_refresh))
        db.execute('UPDATE archive_metadata SET last_partial_refresh_date = current_date')

    logging.info("Update complete.")


def generate_all_items():
    for idx, item in enumerate(search_items('collection:aqueous').iter_as_items()):
        if idx and idx % 20 == 0:
            logging.info(f"Generated {idx} items.")
        yield item.identifier, item.item_metadata['metadata']['date'], link_from_wikilink(item.wikilink)


def generate_added_items_in_date_range(_from: str, _to: str=None):
    date_query = get_date_query(_from, _to)
    for idx, item in enumerate(search_items(f'collection:aqueous AND addeddate:{date_query}]').iter_as_items()):
        if idx % 20 == 0:
            logging.info(f"Generated {idx} items.")
        yield item.identifier, item.item_metadata['metadata']['date'], link_from_wikilink(item.wikilink)


def archive_recording(date: str) -> str:
    with Database() as db:
        rows = db.query("SELECT url FROM archive_items WHERE date_text = ? ORDER BY aid ASC", (date,))
        try:
            return next(rows)[0]
        except StopIteration:
            return ''


def get_date_query(_from, _to=None) -> str:
    return f'[{_from or "null"} TO {_to or "null"}]'


def link_from_wikilink(wikilink):
    # We want everything after the first space and until the second, minus the leading [
    parts = wikilink.split(' ')
    return parts[1].lstrip('[')

