### Botplex

A reddit bot which fetches setlist data from http://aqueousband.com, plus show metadata from http://archive.org and http://nugs.net to provide quick access to setlists and live recordings for the band Aqueous.

### Running locally

You can run locally, but you probably shouldn't, because it would also be responding to comments on the live subreddit. However, if you must, you'll need to 
create a `.env` file in the base directory with the following environment variables set:

```bash
export BOTPLEX_USERNAME=""
export BOTPLEX_PASSWORD=""
export BOTPLEX_CLIENT_ID=""
export BOTPLEX_CLIENT_SECRET=""
export BOTPLEX_USER_AGENT=""
export ARCHIVE_EMAIL=""
export ARCHIVE_PASSWORD=""
export PGHOST=""
export PGPORT=""
export PGUSER=""
export PGPASSWORD=""
export PGDATABASE=""
``` 

You'll also need to install the python `internetarchive` package and run `ia configure`, and copy the resulting config file into
the base directory. Finally, you should create a postgres instance somewhere and put the credentials in the .env file, too.

When the app is running, it exposes a basic flask app on port 8001 which will show you metadata refresh times and recent reply activity. You can 
start metadata refreshes from this page, as well. These tasks are scheduled with `apscheduler` so they will run automatically at intervals, including the loop where the bot checks for reddit comments and responds to them.
There's no authentication, so make sure it's running somewhere safe from prying eyes.

All logs are written to stdout and `BASEDIR/logs/botplex.log`.

### Requirements

On Linux / OSX, you'll need the PostgreSQL development headers installed (libpq-dev). Then install the requirements from requirements.txt and run `python main.py`, or just use
the `./run.sh` script to run the app with `docker`.
