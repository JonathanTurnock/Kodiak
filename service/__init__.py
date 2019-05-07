from repository import PipelineRepository
from ae_runner_application import pipeline_repo
from model import Pipeline
from typing import List

class PipelineService(object):
    def __init__(self):
        self.pipeline_repo: PipelineRepository = pipeline_repo

    def createPipeline(self, url: str) -> Pipeline:
        return self.pipeline_repo.save(Pipeline(url))

    def getPipelines(self) -> List[Pipeline]:
        return self.pipeline_repo.findAll()