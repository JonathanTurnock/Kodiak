from datetime import datetime
from typing import List

from kodiak.agent.callback.handler import do_callback
from kodiak.agent.model.job import Job
from kodiak.agent.model.status import Status
from kodiak.utils.id import new_string_id


class Run:
    def __init__(self, job):
        self.uuid: str = new_string_id()
        self.job: Job = job
        self._status: Status = Status.PENDING
        self.started: datetime = datetime.now()
        self.ended: datetime = None
        self.steps: List[Step] = []
        do_callback(self)

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'jobId': self.job.uuid,
            'status': self.status.name,
            'started': self.started.isoformat(),
            'ended': self.ended.isoformat() if self.ended is not None else None
        }

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status
        do_callback(self)


class Step:
    def __init__(self, run, number, name, image):
        self.run: Run = run
        self.number: int = number
        self.name: str = name
        self.image: str = image
        self._status: Status = Status.PENDING
        self.commands: List[Command] = []
        do_callback(self)

    def to_dict(self):
        return {
            'runId': self.run.uuid,
            'number': self.number,
            'name': self.name,
            'image': self.image,
            'status': self.status.name,
        }

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status
        do_callback(self)


class Command:
    def __init__(self, step, number, instruction):
        self.step: Step = step
        self.number: int = number
        self.instruction: str = instruction
        self.std_out: List[str] = []
        self.std_err: List[str] = []
        do_callback(self)

    def add_output(self, output):
        self.std_out.append(output)
        do_callback(self)

    def add_error(self, error):
        self.std_err.append(error)
        do_callback(self)

    def to_dict(self):
        return {
            'runId': self.step.run.uuid,
            'stepNumber': self.step.number,
            'number': self.number,
            'instruction': self.instruction,
            'stdOut': "".join(self.std_out),
            'stdErr': "".join(self.std_err)
        }
