import logging
from typing import Dict

LOGGER = logging.getLogger(__name__)


class Job:
    def __init__(self, name: str, url: str):
        self.id = None
        self.name = name
        self.url = url

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url
        }

    @staticmethod
    def of_dict(_dict: Dict):
        job = Job(
            _dict["name"],
            _dict["url"]
        )
        if "id" in _dict.keys():
            job.id = _dict["id"]
        return job
