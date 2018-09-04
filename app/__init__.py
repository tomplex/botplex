import os
import boto3
import atexit
import dotenv

from pathlib import Path

appdir = Path(__file__).parent
basedir = appdir.parent

dotenv.load_dotenv(str(basedir / '.env'))


from flask import Flask

app = Flask(__name__)

env = os.environ.get('FLASK_ENV', 'development')

if env == 'production':
    # Download the database file from S3, and register a helper to upload the file to S3 when we exit
    s3 = boto3.client('s3')
    database_file_name = env + '.sqlite'
    database_file_path = str(basedir / database_file_name)
    s3_bucket = str(os.environ.get('S3_BUCKET_NAME'))

    s3.download_file(s3_bucket, database_file_name, database_file_path)
    atexit.register(lambda: s3.upload_file(database_file_path, s3_bucket, database_file_name))

from app import routes
