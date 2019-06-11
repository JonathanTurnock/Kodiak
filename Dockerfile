FROM python:3

ENV PYTHONUNBUFFERED=1

ENV LOG_LEVEL=info

COPY . /opt/fxq/ae-runner

RUN pip install gunicorn && pip install /opt/fxq/ae-runner

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "fxq.ae.runner.wsgi", "--log-level", "${LOG_LEVEL}"]