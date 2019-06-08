import logging
import os
import shutil

import yaml
from fxq.core.beans.factory.annotation import Autowired
from fxq.core.stereotype import Service
from git import Repo

from fxq.ae.runner import constants
from fxq.ae.runner.marshaller import GitUrlMarshaller, PipelineFactory
from fxq.ae.runner.model import Executor, Pipeline
from fxq.ae.runner.model.PipelineStatus import PipelineStatus
from fxq.ae.runner.repository import ExecutorRepository, PipelineRepository
from fxq.ae.runner.service import DockerService, PipelineService

LOGGER = logging.getLogger(__name__)


@Service
class ExecutorService:

    @Autowired
    def __init__(
            self,
            executor_repository: ExecutorRepository,
            git_url_marshaller: GitUrlMarshaller,
            docker_service: DockerService,
            pipeline_factory: PipelineFactory,
            pipeline_service: PipelineService,
            pipeline_repository: PipelineRepository
    ):
        self.executor_repository = executor_repository
        self.git_url_marshaller = git_url_marshaller
        self.docker_service = docker_service
        self.pipeline_factory = pipeline_factory
        self.pipeline_service = pipeline_service
        self.pipeline_repository: PipelineRepository = pipeline_repository
        LOGGER.info("System Pipeline Base  set to %s" % constants.PIPELINE_BASE)

    def save(self, executor: Executor) -> Executor:
        return self.executor_repository.save(executor)

    def find_all(self):
        return self.executor_repository.find_all()

    def find_by_id(self, executor_id):
        return self.executor_repository.find_by_id(executor_id)

    def start(self, executor: Executor) -> Executor:
        workspace_path = self._get_workspace_path(executor.owner, executor.repo)
        repo = self._clone_repo(executor.url, workspace_path)
        pipeline = self._get_pipeline_from_yml("%s-%s" % (executor.owner, executor.repo),
                                               "%s/%s" % (workspace_path, constants.PIPELINE_YML_NAME))

        pipeline = self.pipeline_repository.save(pipeline)
        pipeline.status = PipelineStatus.IN_PROGRESS
        self.pipeline_service.start(pipeline, workspace_path)
        pipeline.status = PipelineStatus.SUCCESSFUL
        try:
            if pipeline.commit_changes:
                repo.git.add('--all')
                repo.git.commit(message="FXQ Pipeline Commit")
                repo.git.push()
        except KeyError:
            pass
        except Exception as e:
            LOGGER.error("Failed to commit changes ", e)

        shutil.rmtree(workspace_path)
        return executor

    def _get_workspace_path(self, owner, name) -> str:
        return "%s/%s/%s/%s" % (
            constants.PIPELINE_BASE,
            constants.PROJECTS_FOLDER,
            owner,
            name
        )

    def _clone_repo(self, url: str, workspace_path: str) -> Repo:
        if os.path.exists(workspace_path): shutil.rmtree(workspace_path)
        return Repo.clone_from(url, workspace_path)

    def _get_pipeline_from_yml(self, name: str, yml_path: str) -> Pipeline:
        with open(yml_path) as ymlf:
            return self.pipeline_factory.pipeline_of(name, yaml.load(ymlf, Loader=yaml.SafeLoader))
