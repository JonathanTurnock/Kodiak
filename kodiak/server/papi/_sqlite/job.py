import logging
from sqlite3 import IntegrityError
from typing import List, Tuple

from kodiak.server.papi._sqlite._interfaces import Dto
from kodiak.server.papi._sqlite.connection_factory import sql_fetch, FetchOneException, sql_commit
from kodiak.server.papi.exception import NoResultException

LOGGER = logging.getLogger(__name__)


class JobDto(Dto):
    def __init__(
            self,
            id: int = None,
            uuid: str = None,
            name: str = None,
            url: str = None
    ):
        self._id: int = id
        self._uuid: str = uuid
        self._name: str = name
        self._url: str = url

    @property
    def id(self):
        return self._id

    @property
    def uuid(self):
        return self._uuid

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url

    def parameterize(self):
        return {
            "id": self._id,
            "uuid": self._uuid,
            "name": self._name,
            "url": self._url
        }


class JobDao:
    _INSERT_JOB = "insert into job (uuid, name, url) values (:uuid, :name, :url)"
    _UPDATE_JOB = "update job set uuid=:uuid, name=:name, url=:url where id=:id"
    _DELETE_JOB = "delete from job where id=?"
    _FIND_JOB_BY_ID = "select id, uuid, name, url from job where id = ?"
    _FIND_JOB_BY_UUID = "select id, uuid, name, url from job where uuid = ?"
    _FIND_ALL_JOBS = "select id, uuid, name, url from job"

    @staticmethod
    def save(job: JobDto) -> JobDto:
        try:
            return JobDao._do_insert(job)
        except IntegrityError as e:
            return JobDao._do_update(job)

    @staticmethod
    def delete(job: JobDto) -> None:
        with sql_commit(JobDao._DELETE_JOB, [job.id]):
            LOGGER.debug(f"Removed Job with id: {job.id}")

    @staticmethod
    def find_job_by_id(id: int) -> JobDto:
        try:
            with sql_fetch(JobDao._FIND_JOB_BY_ID, [id], row_mapper=JobDao._map_full_row, size=1) as job_dto:
                return job_dto
        except FetchOneException:
            raise NoResultException(f"No Job Found with id: {id}") from None

    @staticmethod
    def find_job_by_uuid(uuid: str) -> JobDto:
        try:
            with sql_fetch(JobDao._FIND_JOB_BY_UUID, [uuid], row_mapper=JobDao._map_full_row, size=1) as job_dto:
                return job_dto
        except FetchOneException:
            raise NoResultException(f"No Job Found with uuid: {uuid}") from None

    @staticmethod
    def find_jobs() -> List[JobDto]:
        with sql_fetch(JobDao._FIND_ALL_JOBS, [], row_mapper=JobDao._map_full_row, size=0) as jobs:
            return jobs

    @staticmethod
    def _map_full_row(row: Tuple) -> JobDto:
        _id, _uuid, _name, _url = row
        return JobDto(id=_id, uuid=_uuid, name=_name, url=_url)

    @staticmethod
    def _do_insert(job: JobDto) -> JobDto:
        with sql_commit(JobDao._INSERT_JOB, job.parameterize()) as last_row_id:
            if last_row_id > 0:
                LOGGER.debug(f"Added or replaced job with id: {last_row_id}")
                return JobDao.find_job_by_id(last_row_id)

    @staticmethod
    def _do_update(job: JobDto) -> JobDto:
        existing_row = JobDao.find_job_by_uuid(job.uuid)
        updated_row = JobDto(
            id=existing_row.id,
            uuid=existing_row.uuid,
            name=job.name if job.name is not None else existing_row.name,
            url=job.url if job.url is not None else existing_row.url
        )
        with sql_commit(JobDao._UPDATE_JOB, updated_row.parameterize()) as last_row_id:
            LOGGER.debug(f"Updated existing job with id: {existing_row.id}")
            return updated_row
