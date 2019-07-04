import os
loglevel = os.environ['LOG_LEVEL'] if 'LOG_LEVEL' in os.environ else 'info'
bind = '0.0.0.0:5000'
workers = 5
threads = 2