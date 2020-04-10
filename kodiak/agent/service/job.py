import logging
import os
import shutil
import threading

from git import Repo

import constants
from kodiak.agent.factory.run import RunFactory
from kodiak.agent.model.job import Job
from kodiak.agent.model.run import Run
from kodiak.agent.service.docker import DockerService
from kodiak.agent.service.run import RunService
from kodiak.utils.id import new_string_id

LOGGER = logging.getLogger(__name__)


class JobService:

    def __init__(self, run_service, docker_service):
        self.run_service: RunService = run_service
        self.docker_service: DockerService = docker_service
        LOGGER.info("System Pipeline Base set to %s" % constants.PIPELINE_BASE)

    def process_request(self, job: Job) -> Run:
        LOGGER.info("Processing Request %s" % job.name)
        run = RunFactory.prepare(job)
        t = threading.Thread(target=self._run, args=(run,))
        t.start()
        return run

    def _run(self, run: Run):
        workspace_path = JobService._get_workspace_path()
        JobService._clone_repo(run.job.git_url, workspace_path)
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
