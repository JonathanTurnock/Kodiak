import logging

from fxq.ae.runner.constants import LOGGING_FORMAT
from fxq.ae.runner.fxq_ae_runner_app import app

logging.basicConfig(format=LOGGING_FORMAT, level=logging.getLogger('gunicorn.error').level)
application = app
