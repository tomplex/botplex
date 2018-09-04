import logging
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app import archive_manager, nugs_manager
from app import actions


def setup_scheduler():
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.start()
    atexit.register(scheduler.shutdown)

    logging.info("Adding scheduler jobs")
    scheduler.add_job(
        func=actions.reddit_bot_loop,
        trigger=IntervalTrigger(minutes=5),
        id='reddit_loop',
        name='Check for new reddit comments and respond',
        replace_existing=True)

    scheduler.add_job(
        func=archive_manager.run_metadata_update,
        trigger=IntervalTrigger(weeks=1),
        id='archive_full_update',
        name='Run full Archive metadata update',
        replace_existing=True
    )

    scheduler.add_job(
        func=lambda: archive_manager.run_metadata_update(update_type='partial'),
        trigger=IntervalTrigger(days=1),
        id='archive_partial_update',
        name='Run partial Archive metadata update',
        replace_existing=True
    )

    scheduler.add_job(
        func=nugs_manager.run_full_metadata_update,
        trigger=IntervalTrigger(hours=2),
        id='nugs_full_update',
        name='Run full nugs metadata update',
        replace_existing=True
    )
