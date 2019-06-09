import logging

from fxq.ae.runner.model import Command
from fxq.ae.runner.model.PipelineStatus import PipelineStatus

LOGGER = logging.getLogger(__name__)


class Step:
    def __init__(self, name: str, image: str, status: PipelineStatus = PipelineStatus.PENDING,
                 commit_changes: bool = False):
        self.name = name
        self.image = image
        self._status = status
        self.commit_changes = commit_changes
        self.script = []

    def __repr__(self):
        return str({
            'name': self.name,
            'image': self.image,
            'status': self.status.name,
            'commit_changes': self.commit_changes,
            'script': self.script
        })

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status
        LOGGER.debug("CALLBACK:%s" % self)

    def add_script_command(self, command: Command):
        self.script.append(command)
