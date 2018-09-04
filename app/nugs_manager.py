import logging

import requests

from app.database import Database

nugs_aqueous_search_json = 'http://nugs.net/api.aspx?orgn=nnsite&method=catalog.search&searchStr=aqueous'


def lpad_0(input_str):
    if len(input_str) == 1:
        return '0' + input_str
    else:
        return input_str


def get_search_json() -> dict:
    r = requests.get(nugs_aqueous_search_json)
    return r.json()


def run_full_metadata_update():
    logging.info("Run full metadata update called.")
    with Database() as db:
        in_progress = int(db.query("SELECT refresh_in_progress FROM nugs_metadata")[0])

        if in_progress:
            logging.info("Skipping update.")
            return

        db.execute('UPDATE nugs_metadata SET refresh_in_progress = 1')

    nugs_json = get_search_json()
    logging.info('Got Nugs search results')
    search_results = nugs_json['Response']['catalogSearchTypeContainers'][0]['catalogSearchContainers'][0]['catalogSearchResultItems']

    def result_iterator():
        for result in search_results:
            if not result['performanceDate']:
                continue
            mo, day, yr = result['performanceDate'].split('/')
            yield '-'.join([yr, lpad_0(mo), lpad_0(day)]), 'http://nugs.net' + result['pageURL']

    with Database() as db:
        logging.info("Starting DB load.")
        db.execute('DELETE FROM nugs_items')
        db.cursor.executemany('INSERT INTO nugs_items (date_text, url) VALUES (?, ?)', result_iterator())
        db.execute('UPDATE nugs_metadata SET last_refresh_date = current_timestamp, refresh_in_progress = 0 ')

    logging.info("Completed DB load for nugs data.")


def nugs_recording_url(date: str) -> str:
    with Database() as db:
        try:
            return db.query('SELECT url FROM nugs_items WHERE date_text = ?', (date,))[0]
        except IndexError:
            return ''