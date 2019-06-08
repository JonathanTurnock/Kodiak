import logging
from http import HTTPStatus

from flask import Blueprint, request
from fxq.core.beans.factory.annotation import Autowired
from fxq.core.stereotype import Controller
from fxqwebcore.web.bind.annotation import ResponseBody

from fxq.ae.runner.factory import ExecutorFactory
from fxq.ae.runner.model import Executor
from fxq.ae.runner.service import ExecutorService

LOGGER = logging.getLogger(__name__)


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

    @ResponseBody
    def start(self, executor_id: int):
        return self.executor_service.start(self.executor_service.find_by_id(executor_id))


__controller: ExecutorApiController = Autowired(type=ExecutorApiController)
__factory: ExecutorFactory = Autowired(type=ExecutorFactory)

executor_api_controller = Blueprint('executor_api_controller', __name__)


@executor_api_controller.route('/api/executors', methods=['POST'])
def save():
    try:
        return __controller.save(__factory.from_url(request.json["url"]))
    except KeyError as e:
        LOGGER.error("Error while parsing request data to Executor instance", e)
        return "Missing Required Key %s" % e, HTTPStatus.BAD_REQUEST


@executor_api_controller.route('/api/executors/<int:executor_id>/start', methods=['GET'])
def start(executor_id):
    try:
        return __controller.start(executor_id)
    except KeyError as e:
        LOGGER.error("Failed to start executor as it does not exist", e)
        return "Executor Not found", HTTPStatus.BAD_REQUEST


@executor_api_controller.route('/api/executors', methods=['GET'])
def find_all():
    return __controller.find_all()
