import logging
from typing import Dict

from kodiak.utils.id import new_string_id

LOGGER = logging.getLogger(__name__)


class Job:
    def __init__(self, name: str, url: str):
        self.id = None
        self.uuid = new_string_id()
        self.name = name
        self.url = url

    def to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'name': self.name,
            'url': self.url
        }

    @staticmethod
    def of_dict(_dict: Dict):
        job = Job(
            _dict["name"],
            _dict["url"]
        )
        if "uuid" in _dict.keys():
            job.uuid = _dict["uuid"]
        return job
