import json
import logging
import os
import uuid

import requests

from fxq.ae.runner.constants import JSON_HEADERS, URI_LIST_HEADERS
from fxq.ae.runner.model import Step

LOGGER = logging.getLogger(__name__)

try:
    callback_url = os.environ["CMD_CALLBACK_URL"]
except KeyError:
    callback_url = None


class Command:
    def __init__(
            self,
            step: Step,
            number: int,
            instruction: str
    ):
        self.step = step
        self.number = number
        self.instruction = instruction
        self.output = []
        self.link = self._get_callback_link() if callback_url else None
        self.id = self._get_id()

    def append_output(self, output):
        self.output.append(output)
        print("CALLBACK:%s" % self)
        if callback_url is not None:
            try:
                requests.patch(
                    self.link,
                    data=json.dumps(self.__json__()),
                    headers=JSON_HEADERS)
            except Exception as e:
                LOGGER.error("Callback failed with error", e)

    def __repr__(self):
        return str(self.__json__())

    def __json__(self):
        return {
            'number': self.number,
            'instruction': self.instruction,
            'output': [str(o) for o in self.output]
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
        requests.put("%s/step" % link, data=self.step.link, headers=URI_LIST_HEADERS)
        return link
