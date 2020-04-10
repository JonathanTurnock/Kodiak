import logging

from kodiak.utils.id import new_string_id

LOGGER = logging.getLogger(__name__)


class Job:
    def __init__(self, name: str, git_url: str):
        self.uuid = new_string_id()
        self.name = name
        self.git_url = git_url

    def to_dict(self):
        return {
            'name': self.name,
            'gitUrl': self.git_url
        }

    @staticmethod
    def of_dict(_dict):
        job = Job(
            _dict["name"],
            _dict["gitUrl"]
        )
        return job
