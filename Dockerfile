FROM python:3

ENV PYTHONUNBUFFERED=1

COPY . /opt/fxq/ae-runner

RUN pip install /opt/fxq/ae-runner

EXPOSE 5000

CMD ["fxq-ae-runner", "--debug"]