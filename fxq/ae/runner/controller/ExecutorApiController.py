import logging
from http import HTTPStatus

from flask import request
from fxq.core.beans.factory.annotation import Autowired
from fxq.core.stereotype import Controller
from fxqwebcore.web.bind.annotation import ResponseBody

from fxq.ae.runner.ae_runner_application import app
from fxq.ae.runner.factory import ExecutorFactory
from fxq.ae.runner.model import Executor
from fxq.ae.runner.service import ExecutorService

LOGGER = logging.getLogger("ApiController")


@Controller
class ExecutorApiController:

    @Autowired
    def __init__(self, executor_service: ExecutorService):
        self.executor_service: ExecutorService = executor_service

    @ResponseBody
    def save(self, executor: Executor):
        return self.executor_service.save(executor)

    @ResponseBody
    def find_all(self):
        return self.executor_service.find_all()


# Routing
__controller: ExecutorApiController = Autowired(type=ExecutorApiController)
__factory: ExecutorFactory = Autowired(type=ExecutorFactory)


@app.route('/api/executors', methods=['POST'])
def save():
    try:
        return __controller.save(__factory.from_url(request.json["url"]))
    except KeyError as e:
        LOGGER.error("Error while parsing request data to Executor instance", e)
        return "Missing Required Key %s" % e, HTTPStatus.BAD_REQUEST


@app.route('/api/executors', methods=['GET'])
def find_all():
    return __controller.find_all()
