FROM python:3

ENV PYTHONUNBUFFERED=1

COPY . /opt/fxq/ae-runner
COPY gunicorn.py /etc/fxq/ae-runner/gunicorn.py

RUN pip install gunicorn && pip install /opt/fxq/ae-runner

EXPOSE 5000

CMD ["gunicorn", "-c", "/etc/fxq/ae-runner/gunicorn.py", "fxq.ae.runner.wsgi"]