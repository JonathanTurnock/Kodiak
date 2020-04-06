import logging

from kodiak.app import app
from kodiak.constants import LOGGING_FORMAT

logging.basicConfig(format=LOGGING_FORMAT, level=logging.getLogger('gunicorn.error').level)
application = app
