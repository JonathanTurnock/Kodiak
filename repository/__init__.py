from model import Pipeline
import copy
from typing import List

class PipelineRepository(object):
    def __init__(self):
        self.pipelines = []

    def save(self, pipeline: Pipeline) -> Pipeline:
        self.pipelines.append(pipeline)
        return pipeline

    def findAll(self) -> List[Pipeline]:
        return copy.deepcopy(self.pipelines)