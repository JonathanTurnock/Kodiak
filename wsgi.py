import logging

from app import app
from constants import LOGGING_FORMAT

logging.basicConfig(format=LOGGING_FORMAT, level=logging.getLogger('gunicorn.error').level)
application = app
