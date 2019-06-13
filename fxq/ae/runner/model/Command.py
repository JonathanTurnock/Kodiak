import json
import logging
import os
import uuid

import requests

from fxq.ae.runner.constants import JSON_HEADERS

LOGGER = logging.getLogger(__name__)


class Command:
    def __init__(
            self,
            step_id: str,
            cmd_no: int,
            instruction: str
    ):
        self.cmd_id = str(uuid.uuid4())
        self.cmd_no = cmd_no
        self.step_id = step_id
        self.instruction = instruction
        self.output = []

    def append_output(self, output):
        self.output.append(output)
        print("CALLBACK:%s" % self)
        try:
            requests.post(os.environ["CMD_CALLBACK_URL"], data=json.dumps(self.__json__()), headers=JSON_HEADERS)
        except KeyError as e:
            LOGGER.warning("No Command callback url defined. Set CMD_CALLBACK_URL as an environment variable to enable"
                        " the callback functionality for commands.")
        except Exception as e:
            LOGGER.error("Callback failed with error", e)

    def __repr__(self):
        return str(self.__json__())

    def __json__(self):
        return {
            'cmd_id': self.cmd_id,
            'step_id': self.step_id,
            'cmd_no': self.cmd_no,
            'instruction': self.instruction,
            'output': [str(o) for o in self.output]
        }
