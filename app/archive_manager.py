import logging

from internetarchive import search_items

from app.database import Database
from app import basedir


def archive_search(qry):
    return search_items(qry, config_file=str(basedir / 'ia.ini'))


def run_metadata_update(update_type='full'):
    logging.info(f"Running {update_type} Archive metadata update")
    with Database() as db:
        try:
            if db.query('SELECT refresh_in_progress FROM archive_metadata')[0]:
                logging.info("Skipping update due to in-progress refresh")
                return

            db.execute("UPDATE archive_metadata SET refresh_in_progress = TRUE")
            db.commit()

            if update_type == 'full':
                db.execute('DELETE FROM archive_items')
                generator = generate_all_items()
            else:
                last_partial_refresh = str(db.query('SELECT last_partial_refresh_date FROM archive_metadata')[0])
                logging.info(f"Looking for shows added since last update at {last_partial_refresh}")
                generator = generate_added_items_in_date_range(last_partial_refresh)

            db.cursor.executemany('INSERT INTO archive_items (aid, date_text, url) VALUES (%s, %s, %s)', generator)
            db.execute(f'UPDATE archive_metadata SET last_{update_type}_refresh_date = current_timestamp')

        finally:
            db.execute(f'UPDATE archive_metadata SET refresh_in_progress = FALSE')
            logging.info("Update complete.")


def generate_all_items():
    for idx, item in enumerate(archive_search('collection:aqueous').iter_as_items()):
        if idx and idx % 20 == 0:
            logging.info(f"Generated {idx} items.")
        yield item.identifier, item.item_metadata['metadata']['date'], link_from_wikilink(item.wikilink)


def generate_added_items_in_date_range(_from: str, _to: str=None):
    date_query = get_date_query(_from, _to)
    for idx, item in enumerate(archive_search(f'collection:aqueous AND addeddate:{date_query}]').iter_as_items()):
        if idx % 20 == 0:
            logging.info(f"Generated {idx} items.")
        yield item.identifier, item.item_metadata['metadata']['date'], link_from_wikilink(item.wikilink)


def archive_recording(date: str) -> str:
    with Database() as db:
        rows = db.query("SELECT url FROM archive_items WHERE date_text = %s ORDER BY aid ASC", (date,))
        try:
            return rows[0]
        except (IndexError):
            return ''


def get_date_query(_from, _to=None) -> str:
    return f'[{_from or "null"} TO {_to or "null"}]'


def link_from_wikilink(wikilink):
    # We want everything after the first space and until the second, minus the leading [
    parts = wikilink.split(' ')
    return parts[1].lstrip('[')

