__author__ = 'tom caruso'


import dotenv
from pathlib import Path

appdir = Path(__file__).parent
basedir = appdir.parent

dotenv.load_dotenv(str(basedir / '.env'))

from flask import Flask

app = Flask(__name__)

from app import routes
