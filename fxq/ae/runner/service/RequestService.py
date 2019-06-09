import logging
import os
import shutil
import threading
import uuid

from fxq.core.beans.factory.annotation import Autowired
from fxq.core.stereotype import Service
from git import Repo

from fxq.ae.runner import constants
from fxq.ae.runner.model import Request, Pipeline
from fxq.ae.runner.model.PipelineStatus import PipelineStatus
from fxq.ae.runner.service import DockerService, PipelineService

LOGGER = logging.getLogger(__name__)


@Service
class RequestService:

    @Autowired
    def __init__(
            self,
            pipeline_service: PipelineService,
            docker_service: DockerService
    ):
        self.pipeline_service = pipeline_service
        self.docker_service = docker_service
        LOGGER.info("System Pipeline Base set to %s" % constants.PIPELINE_BASE)

    def process_request(self, request: Request) -> Pipeline:
        LOGGER.info("Processing Request %s" % request)
        workspace_path = RequestService._get_workspace_path(request.owner, request.repo)
        RequestService._clone_repo(request.url, workspace_path)
        pipeline = Pipeline.of_yml_file_with_name("%s-%s" % (request.owner, request.repo),
                                                  "%s/%s" % (workspace_path, constants.PIPELINE_YML_NAME))
        t = threading.Thread(target=self.run, args=(pipeline, workspace_path))
        t.start()
        return pipeline

    def run(self, pipeline: Pipeline, workspace_path: str):
        LOGGER.info("Starting a new Pipeline Thread for pipeline run id %s" % pipeline.run_id)
        pipeline.status = PipelineStatus.IN_PROGRESS
        self.pipeline_service.start(pipeline, workspace_path)
        pipeline.status = PipelineStatus.SUCCESSFUL
        shutil.rmtree(workspace_path)
        LOGGER.info("Finishing Pipeline Thread for pipeline run id %s" % pipeline.run_id)

    @staticmethod
    def _get_workspace_path(owner, name) -> str:
        return "%s/%s/%s/%s/%s" % (
            constants.PIPELINE_BASE,
            constants.PROJECTS_FOLDER,
            owner,
            name,
            uuid.uuid4()
        )

    @staticmethod
    def _clone_repo(url: str, workspace_path: str) -> Repo:
        if os.path.exists(workspace_path): shutil.rmtree(workspace_path)
        return Repo.clone_from(url, workspace_path)
