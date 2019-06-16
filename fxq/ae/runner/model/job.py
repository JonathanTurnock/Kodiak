import logging

LOGGER = logging.getLogger(__name__)


class ScmRepo:
    def __init__(self, url):
        self.url: str = url


class Job:
    def __init__(self, name: str, scm_repo: ScmRepo):
        self.name = name
        self.scm_repo = scm_repo
        self._links = None

    def to_dict(self):
        return {
            'name': self.name,
            'scmRepo': self.scm_repo
        }

    @staticmethod
    def of_dict(_dict):
        job = Job(
            _dict["name"],
            ScmRepo(_dict["scmRepo"]["url"])
        )
        try:
            job._links = _dict["_links"]
        except KeyError:
            LOGGER.info("No Links detected for Job")
        return job
