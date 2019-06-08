from fxq.core.stereotype import Component

from fxq.ae.runner.model import Pipeline


@Component
class PipelineRepository:
    sequence = 0

    def __init__(self):
        self._pipelines = {}

    def save(self, pipeline: Pipeline) -> Pipeline:
        PipelineRepository.sequence += 1
        pipeline.id = PipelineRepository.sequence
        self._pipelines[pipeline.id] = pipeline
        return pipeline

    def update(self, pipeline):
        self._pipelines[pipeline.id] = pipeline
        return pipeline

    def find_by_id(self, id):
        return self._pipelines[id]

    def find_all(self):
        return self._pipelines.values()
