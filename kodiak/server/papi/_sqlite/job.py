import logging
from typing import List, Tuple

from kodiak.server.papi._sqlite.connection_factory import sql_fetch, FetchOneException, sql_commit
from kodiak.server.papi._sqlite.exception import NoResultException

LOGGER = logging.getLogger(__name__)


class JobDto(object):
    def __init__(
            self,
            id: int = None,
            name: str = None,
            url: str = None
    ):
        self._id: int = id
        self._name: str = name
        self._url: str = url

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url


class JobDao:
    _INSERT_NEW_JOB = "insert into job (name, url) values (?, ?)"
    _UPDATE_EXISTING_JOB = "update job set name=?, url=? where id=?"
    _FIND_JOB_BY_ID = "select id, name, url from job where id = ?"
    _FIND_ALL_JOBS = "select id, name, url from job"

    @staticmethod
    def map_full_row(row: Tuple) -> JobDto:
        _id, _name, _url = row
        return JobDto(id=_id, name=_name, url=_url)

    @staticmethod
    def save(job: JobDto) -> JobDto:
        with sql_commit(JobDao._INSERT_NEW_JOB, [job.name, job.url]) as last_row_id:
            LOGGER.info(f"Added new job with with id: {last_row_id}")
            return JobDao.find_job_by_id(last_row_id)

    @staticmethod
    def find_job_by_id(id: int) -> JobDto:
        try:
            with sql_fetch(JobDao._FIND_JOB_BY_ID, [id], row_mapper=JobDao.map_full_row, size=1) as job_dto:
                return job_dto
        except FetchOneException:
            raise NoResultException(f"No Job Found with id: {id}") from None

    @staticmethod
    def find_jobs() -> List[JobDto]:
        with sql_fetch(JobDao._FIND_ALL_JOBS, [], row_mapper=JobDao.map_full_row, size=0) as jobs:
            return jobs
