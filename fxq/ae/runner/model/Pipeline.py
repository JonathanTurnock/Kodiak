import logging
import uuid
from typing import List

import yaml

from fxq.ae.runner.model.Command import Command
from fxq.ae.runner.model.PipelineStatus import PipelineStatus
from fxq.ae.runner.model.Step import Step

LOGGER = logging.getLogger(__name__)


class Pipeline:
    def __init__(self, name: str, status: PipelineStatus = PipelineStatus.PENDING,
                 commit_changes: bool = False):
        self.run_id = str(uuid.uuid4())
        self.name = name
        self._status = status
        self.commit_changes = commit_changes
        self.steps: List[Step] = []

    def __repr__(self):
        return str(self.__json__())

    def __json__(self):
        return {
            'run_id': self.run_id,
            'name': self.name,
            'status': self.status.__json__(),
            'commit_changes': self.commit_changes,
            'steps': [s.__json__() for s in self.steps]
        }

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status
        print("CALLBACK:%s" % self)

    def add_step(self, step: Step):
        self.steps.append(step)

    @staticmethod
    def of_yml_file_with_name(name: str, yml_path: str):
        with open(yml_path) as ymlf:
            pipeline_dict = yaml.load(ymlf, Loader=yaml.SafeLoader)
            pipeline = Pipeline(name)
            for s in pipeline_dict["pipelines"]["steps"]:
                step = Step(s["step"]["name"], s["step"]["image"])
                for se in s["step"]["script"]:
                    command = Command(se)
                    step.add_script_command(command)

                pipeline.add_step(step)

            return pipeline
