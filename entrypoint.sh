#!/bin/sh
gunicorn --bind 0.0.0.0:5000 --workers ${WORKERS} --threads=${THREADS} fxq.ae.runner.wsgi --log-level ${LOG_LEVEL}