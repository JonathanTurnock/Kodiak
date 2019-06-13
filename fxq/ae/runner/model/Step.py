import json
import logging
import os
import uuid
from typing import List

import requests

from fxq.ae.runner.constants import JSON_HEADERS, URI_LIST_HEADERS
from fxq.ae.runner.model import Command, Pipeline
from fxq.ae.runner.model.PipelineStatus import PipelineStatus

LOGGER = logging.getLogger(__name__)

try:
    callback_url = os.environ["STEP_CALLBACK_URL"]
except KeyError:
    callback_url = None


class Step:
    def __init__(
            self,
            pipeline: Pipeline,
            number: int,
            name: str,
            image: str,
            status: PipelineStatus = PipelineStatus.PENDING,
            commit_changes: bool = False
    ):
        self.pipeline = pipeline
        self.number = number
        self.name = name
        self.image = image
        self._status = status
        self.commit_changes = commit_changes
        self.script: List[Command] = []
        self.link = self._get_callback_link() if callback_url else None
        self.id = self._get_id()

    def __repr__(self):
        return str(self.__json__())

    def __json__(self):
        return {
            'name': self.name,
            'image': self.image,
            'number': self.number,
            'status': self.status.name,
            'commit': self.commit_changes,
            'script': [s.__json__() for s in self.script]
        }

    def _get_id(self):
        if callback_url is not None:
            return self.link.split("/")[-1]
        else:
            return str(uuid.uuid4())

    def _get_callback_link(self):
        link = requests.post(
            "%s" % callback_url,
            data=json.dumps(self.__json__()),
            headers=JSON_HEADERS).json()["_links"]["self"]["href"]
        requests.put("%s/run" % link, data=self.pipeline.link, headers=URI_LIST_HEADERS)
        return link

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status
        print("CALLBACK:%s" % self)
        if callback_url is not None:
            try:
                requests.patch(
                    self.link,
                    data=json.dumps(self.__json__()),
                    headers=JSON_HEADERS)
            except Exception as e:
                LOGGER.error("Callback failed with error", e)

    def add_script_command(self, command: Command):
        self.script.append(command)
