import logging
from http import HTTPStatus

from flask import Blueprint
from fxq.core.beans.factory.annotation import Autowired
from fxq.core.stereotype import Controller
from fxqwebcore.web.bind.annotation import ResponseBody

from fxq.ae.runner.service import PipelineService

LOGGER = logging.getLogger(__name__)


@Controller
class PipelineApiController:

    @Autowired
    def __init__(self, pipeline_service: PipelineService):
        self.pipeline_service = pipeline_service

    @ResponseBody
    def find_by_id(self, pipeline_id):
        return self.pipeline_service.find_by_id(pipeline_id)

    @ResponseBody
    def find_all(self):
        return self.pipeline_service.find_all()


__controller: PipelineApiController = Autowired(type=PipelineApiController)

pipeline_api_controller = Blueprint('pipeline_api_controller', __name__)


@pipeline_api_controller.route('/api/pipelines', methods=['GET'])
def find_all():
    return __controller.find_all()


@pipeline_api_controller.route('/api/pipelines/<int:pipeline_id>', methods=['GET'])
def get(pipeline_id):
    try:
        return __controller.find_by_id(pipeline_id)
    except KeyError:
        LOGGER.error("Pipeline %s does not exist" % pipeline_id)
        return "Pipeline Not found", HTTPStatus.BAD_REQUEST
