__author__ = 'tom caruso'

import logging

from app import app, schedule, basedir

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(), logging.FileHandler(str(basedir / 'log/botplex.log'))]
)


if __name__ == '__main__':
    logging.info("Starting up.")

    schedule.setup_scheduler()
    app.run('0.0.0.0', port=8000, debug=True, use_reloader=False)
