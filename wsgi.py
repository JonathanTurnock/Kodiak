import logging

from app import app
from bootstrap import LOGGING_FORMAT

logging.basicConfig(format=LOGGING_FORMAT, level=logging.getLogger('gunicorn.error').level)
application = app
