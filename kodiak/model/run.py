from datetime import datetime
from enum import Enum
from typing import List

from kodiak.model.job import Job


class Status(Enum):
    PENDING = 1
    SUCCESSFUL = 2
    FAILED = 3
    IN_PROGRESS = 4
    PAUSED = 5
    STOPPED = 6
    ABORTED = 7

    @staticmethod
    def value_of(name):
        return {
            "PENDING": Status.PENDING,
            "SUCCESSFUL": Status.SUCCESSFUL,
            "FAILED": Status.FAILED,
            "IN_PROGRESS": Status.IN_PROGRESS,
            "PAUSED": Status.PAUSED,
            "STOPPED": Status.STOPPED,
            "ABORTED": Status.ABORTED
        }[name]


class Run:
    def __init__(
            self,
            job: Job = None,
            uuid: str = None,
            status: Status = None,
            started: datetime = None,
            ended: datetime = None,
            steps: List = None
    ):
        self._job: Job = job
        self._uuid: str = uuid
        self._status: Status = status if status is not None else Status.PENDING
        self._started: datetime = started
        self._ended: datetime = ended
        self._steps: List[Step] = steps if steps is not None else []

    @property
    def job(self) -> Job:
        return self._job

    @property
    def uuid(self) -> str:
        return self._uuid

    @property
    def status(self) -> Status:
        return self._status

    @status.setter
    def status(self, status: Status) -> None:
        self._status = status

    @property
    def started(self) -> datetime:
        return self._started

    @started.setter
    def started(self, started: datetime) -> None:
        self._started = started

    @property
    def ended(self) -> datetime:
        return self._ended

    @ended.setter
    def ended(self, ended: datetime) -> None:
        self._ended = ended

    @property
    def steps(self) -> List:
        return self._steps


class Step:
    def __init__(
            self,
            run: Run = None,
            number: int = None,
            name: str = None,
            image: str = None,
            status: Status = None,
            commands: List = None
    ):
        self._run: Run = run
        self._number: int = number
        self._name: str = name
        self._image: str = image
        self._status: Status = status if status is not None else Status.PENDING
        self._commands: List[Command] = commands if commands is not None else []

    @property
    def run(self) -> Run:
        return self._run

    @property
    def number(self) -> int:
        return self._number

    @property
    def name(self) -> str:
        return self._name

    @property
    def image(self) -> str:
        return self._image

    @property
    def status(self) -> Status:
        return self._status

    @status.setter
    def status(self, status: Status) -> None:
        self._status = status

    @property
    def commands(self) -> List:
        return self._commands


class Command:
    def __init__(
            self,
            step: Step = None,
            number: int = None,
            instruction: str = None,
            std_out: List[str] = None,
            std_err: List[str] = None
    ):
        self._step: Step = step
        self._number: int = number
        self._instruction: str = instruction
        self._std_out: List[str] = std_out if std_out is not None else []
        self._std_err: List[str] = std_err if std_err is not None else []

    @property
    def step(self) -> Step:
        return self._step

    @property
    def number(self) -> int:
        return self._number

    @property
    def instruction(self) -> str:
        return self._instruction

    @property
    def std_out(self) -> List[str]:
        return self._std_out

    @property
    def std_err(self) -> List[str]:
        return self._std_err
