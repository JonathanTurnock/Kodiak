import logging

from fxq.ae.runner.model import Step
from fxq.ae.runner.model.PipelineStatus import PipelineStatus

LOGGER = logging.getLogger(__name__)


class Pipeline:
    def __init__(self, id: int, name: str, status: PipelineStatus = PipelineStatus.PENDING,
                 commit_changes: bool = False):
        self.id = id
        self.name = name
        self._status = status
        self.commit_changes = commit_changes
        self.steps = []

    def __repr__(self):
        return str({
            'id': self.id,
            'name': self.name,
            'status': self.status.name,
            'commit_changes': self.commit_changes,
            'steps': self.steps
        })

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status
        LOGGER.debug("CALLBACK:%s" % self)

    def add_step(self, step: Step):
        self.steps.append(step)
