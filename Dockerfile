FROM python:3

ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL "info"
ENV WORKERS 5
ENV THREADS 2

COPY . /opt/fxq/ae-runner
COPY entrypoint.sh /

RUN pip install gunicorn && pip install /opt/fxq/ae-runner

EXPOSE 5000

ENTRYPOINT ["sh", "-c"]
CMD["exec gunicorn --bind 0.0.0.0:5000 --workers ${WORKERS} --threads=${THREADS} fxq.ae.runner.wsgi --log-level ${LOG_LEVEL}"]