FROM python:3

ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL "info"
ENV WORKERS 5
ENV THREADS 2

COPY . /opt/fxq/ae-runner

RUN pip install gunicorn && pip install /opt/fxq/ae-runner

EXPOSE 5000

CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:5000 --workers ${WORKERS} --threads=${THREADS} fxq.ae.runner.wsgi --log-level ${LOG_LEVEL}"]