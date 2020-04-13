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
            id: int = None,
            job: Job = None,
            uuid: str = None,
            status: Status = None,
            started: datetime = None,
            ended: datetime = None
    ):
        self.ended: datetime = ended

        self.id: int = id
        self.job: Job = job
        self.uuid: str = uuid
        self.status: Status = status
        self.started: datetime = started


class Step:
    def __init__(
            self,
            id: int = None,
            run: Run = None,
            number: int = None,
            name: str = None,
            image: str = None,
            status: Status = None,
    ):
        self.id: int = id
        self.run: Run = run
        self.number: int = number
        self.name: str = name
        self.image: str = image
        self.status: Status = status


class Command:
    def __init__(
            self,
            id: int = None,
            step: Step = None,
            number: int = None,
            instruction: str = None,
            std_out: List[str] = [],
            std_err: List[str] = []
    ):
        self.id: int = id
        self.step: Step = step
        self.number: int = number
        self.instruction: str = instruction
        self.std_out: List[str] = std_out
        self.std_err: List[str] = std_err
