import logging

from fxq.core.beans.factory.annotation import Autowired
from fxq.core.stereotype import Service

from fxq.ae.runner.model import Pipeline
from fxq.ae.runner.model.PipelineStatus import PipelineStatus
from fxq.ae.runner.service import DockerService

LOGGER = logging.getLogger(__name__)


@Service
class PipelineService:

    @Autowired
    def __init__(self, docker_service: DockerService):
        self._docker_service = docker_service

    def start(self, pipeline: Pipeline, workspace_path: str):
        LOGGER.info("Executing Pipeline %s" % pipeline.name)
        for step in pipeline.steps:
            container = None
            try:
                LOGGER.info("Running step %s" % step.name)
                step.status = PipelineStatus.IN_PROGRESS
                container = self._docker_service.provision(
                    pipeline.run_uuid,
                    step.image,
                    workspace_path
                )

                for command in step.script:
                    self._docker_service.run_command(container, command)

                step.status = PipelineStatus.SUCCESSFUL
            except Exception as e:
                LOGGER.error("Error occurred during pipeline", e)
                step.status = PipelineStatus.FAILED
            finally:
                LOGGER.debug("Starting Pipeline Teardown")
                if container is not None:
                    self._docker_service.teardown(container)

            LOGGER.info("Completed running step %s" % step.name)

        LOGGER.info("Completed Executing the Pipeline %s" % pipeline.name)
