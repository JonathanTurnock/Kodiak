import json
import logging
import os
import uuid
from typing import List

import requests
import yaml

from fxq.ae.runner.constants import JSON_HEADERS
from fxq.ae.runner.model.Command import Command
from fxq.ae.runner.model.PipelineStatus import PipelineStatus
from fxq.ae.runner.model.Step import Step

LOGGER = logging.getLogger(__name__)

try:
    callback_url = os.environ["PIPELINE_CALLBACK_URL"]
except KeyError:
    callback_url = None


class Pipeline:
    def __init__(
            self,
            name: str,
            status: PipelineStatus = PipelineStatus.PENDING,
            commit_changes: bool = False
    ):
        self.name = name
        self.run_uuid = str(uuid.uuid4())
        self._status = status
        self.commit_changes = commit_changes
        self.steps: List[Step] = []
        self.link = self._get_callback_link() if callback_url else None
        self.id = self._get_id()

    def __repr__(self):
        return str(self.__json__())

    def __json__(self):
        return {
            'name': self.name,
            'status': self.status.__json__(),
            'commit': self.commit_changes,
            'steps': [s.__json__() for s in self.steps]
        }

    def _get_id(self):
        if callback_url is not None:
            return self.link.split("/")[-1]
        else:
            return str(uuid.uuid4())

    def _get_callback_link(self):
        return requests.post(
            "%s" % callback_url,
            data=json.dumps(self.__json__()),
            headers=JSON_HEADERS).json()["_links"]["self"]["href"]

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

    def add_step(self, step: Step):
        self.steps.append(step)

    @staticmethod
    def of_yml_file_with_name(name: str, yml_path: str):
        with open(yml_path) as ymlf:
            pipeline_dict = yaml.load(ymlf, Loader=yaml.SafeLoader)
            pipeline = Pipeline(name)
            s_no = 0
            for s in pipeline_dict["pipelines"]["steps"]:
                s_no += 1
                step = Step(pipeline, s_no, s["step"]["name"], s["step"]["image"])
                se_no = 0
                for se in s["step"]["script"]:
                    se_no += 1
                    command = Command(step, se_no, se)
                    step.add_script_command(command)

                pipeline.add_step(step)

            return pipeline
