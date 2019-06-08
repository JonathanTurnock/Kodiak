import logging
import os
import shutil

from fxq.core.beans.factory.annotation import Autowired
from fxq.core.stereotype import Service
from git import Repo

from fxq.ae.runner import constants
from fxq.ae.runner.client import DockerClient
from fxq.ae.runner.marshaller import GitUrlMarshaller
from fxq.ae.runner.model import Executor
from fxq.ae.runner.repository import ExecutorRepository

LOGGER = logging.getLogger("ExecutorService")


@Service
class ExecutorService:

    @Autowired
    def __init__(
            self,
            executor_repository: ExecutorRepository,
            git_url_marshaller: GitUrlMarshaller,
            docker_client: DockerClient
    ):
        self.executor_repository = executor_repository
        self.git_url_marshaller = git_url_marshaller
        self.docker_client = docker_client
        LOGGER.info("System Pipeline Base  set to %s" % constants.PIPELINE_BASE)

    def save(self, executor: Executor) -> Executor:
        executor = self.executor_repository.save(executor)
        return self.start(executor)

    def find_all(self):
        return self.executor_repository.find_all()

    def start(self, executor: Executor) -> Executor:
        workspace_path = self._get_workspace_path(executor.owner, executor.repo)
        if os.path.exists(workspace_path): shutil.rmtree(workspace_path)
        repo = Repo.clone_from(executor.url, workspace_path)
        self.docker_client.execute_pipeline_from_repo(repo)
        #shutil.rmtree(workspace_path)
        return executor

    def _get_workspace_path(self, owner, name) -> str:
        return "%s/%s/%s/%s" % (
            constants.PIPELINE_BASE,
            constants.PROJECTS_FOLDER,
            owner,
            name
        )
