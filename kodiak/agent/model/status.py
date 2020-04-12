from enum import Enum
from typing import Dict


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


class Health():
    def __init__(self, status: str, details: Dict = None):
        self.status = status
        self.details = details

    def to_dict(self):
        resp = {
            'status': self.status
        }

        if self.details:
            resp["details"] = self.details

        return resp
