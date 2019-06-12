import json
import logging
import os
import uuid
from typing import List

import requests

from fxq.ae.runner.constants import JSON_HEADERS
from fxq.ae.runner.model import Command
from fxq.ae.runner.model.PipelineStatus import PipelineStatus

LOGGER = logging.getLogger(__name__)


class Step:
    def __init__(
            self,
            run_id: str,
            step_no: int,
            name: str,
            image: str,
            status: PipelineStatus = PipelineStatus.PENDING,
            commit_changes: bool = False
    ):
        self.step_id = str(uuid.uuid4())
        self.step_no = step_no
        self.run_id = run_id
        self.name = name
        self.image = image
        self._status = status
        self.commit_changes = commit_changes
        self.script: List[Command] = []

    def __repr__(self):
        return str(self.__json__())

    def __json__(self):
        return {
            'step_id': self.step_id,
            'run_id': self.run_id,
            'step_no': self.step_no,
            'name': self.name,
            'image': self.image,
            'status': self.status.name,
            'commit_changes': self.commit_changes,
            'script': [s.__json__() for s in self.script]
        }

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status
        print("CALLBACK:%s" % self)
        if os.environ["STEP_CALLBACK_URL"]:
            try:
                requests.post(os.environ["STEP_CALLBACK_URL"], data=json.dumps(self.__json__()), headers=JSON_HEADERS)
            except KeyError as e:
                LOGGER.warning("No Step callback url defined. Set STEP_CALLBACK_URL as an environment variable to enable"
                            " the callback functionality for steps.")
            except Exception as e:
                LOGGER.error("Callback failed with error", e)

    def add_script_command(self, command: Command):
        self.script.append(command)
