import logging
import os
import shutil
import threading

from fxq.core.beans.factory.annotation import Autowired
from fxq.core.stereotype import Service
from git import Repo

import constants
from kodiak.agent.factory.run import RunFactory
from kodiak.model.job import Job
from kodiak.utils.id import new_string_id

LOGGER = logging.getLogger(__name__)


@Service(name="job_service")
class JobService:

    def __init__(self, run_service=Autowired("run_service"), docker_service=Autowired("docker_service")):
        self.run_service = run_service
        self.docker_service = docker_service
        LOGGER.info("System Pipeline Base set to %s" % constants.PIPELINE_BASE)

    def process_request(self, job: Job) -> str:
        """
        Starts a new Run of the given job.

        :param job: Job Object to start the run for
        :return: UUID of the run
        """
        LOGGER.info("Processing Request %s" % job.name)
        run = RunFactory.prepare(job)
        t = threading.Thread(target=self._run, args=(run,))
        t.start()
        return run.uuid

    def _run(self, run):
        workspace_path: str = JobService._get_workspace_path()
        JobService._clone_repo(run.job.url, workspace_path)
        LOGGER.debug("Cloned Repo into Workspace %s" % workspace_path)
        RunFactory.configure_from_yml_file(run, "%s/%s" % (workspace_path, constants.PIPELINE_YML_NAME))
        LOGGER.info("Starting a new run thread for uuid %s" % run.uuid)
        self.run_service.start(run, workspace_path)
        shutil.rmtree(workspace_path)
        LOGGER.info("Finishing run thread for uuid %s" % run.uuid)

    @staticmethod
    def _get_workspace_path() -> str:
        return "%s/%s/%s" % (
            constants.PIPELINE_BASE,
            constants.PROJECTS_FOLDER,
            new_string_id()
        )

    @staticmethod
    def _clone_repo(url: str, workspace_path: str) -> Repo:
        if os.path.exists(workspace_path): shutil.rmtree(workspace_path)
        return Repo.clone_from(url, workspace_path)
