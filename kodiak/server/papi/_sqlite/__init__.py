import logging
import sqlite3
from typing import List

from fxq.core.beans.factory.annotation import Autowired
from fxq.core.stereotype import Repository

from kodiak.model.job import Job
from kodiak.model.run import Run
from kodiak.server.papi._sqlite.command import command_dto_of_command, CommandDao, CommandDto
from kodiak.server.papi._sqlite.job import JobDto, JobDao
from kodiak.server.papi._sqlite.run import RunDto, run_dto_of_run, RunDao
from kodiak.server.papi._sqlite.schema import SchemaInterface
from kodiak.server.papi._sqlite.step import step_dto_of_step, StepDao, StepDto
from kodiak.server.papi.repos import JobRepository, RunRepository
from kodiak.utils.version import is_same_or_later_version

MIN_SQLITE_VERSION = "3.22.0"

LOGGER = logging.getLogger(__name__)

sqlite_version = sqlite3.sqlite_version
LOGGER.info(f"Running SQLite Version {sqlite_version}")
if not is_same_or_later_version(sqlite_version, MIN_SQLITE_VERSION):
    raise Exception(f"SQLite version {sqlite_version} is not valid, requires minimum of {MIN_SQLITE_VERSION}")

schema_interface: SchemaInterface = Autowired("schema_interface")
schema_interface.check_for_updates()


@Repository(name="job_repository")
class SqliteJobRepository(JobRepository):

    def save(self, job: Job) -> Job:
        job_dto = JobDao.save(SqliteJobRepository._to_dto(job))
        return SqliteJobRepository._to_job(job_dto)

    def delete_by_uuid(self, uuid: str) -> None:
        JobDao.delete_by_uuid(uuid)

    def find_all(self) -> List[Job]:
        return [SqliteJobRepository._to_job(job_dto) for job_dto in JobDao.find_jobs()]

    def find_by_uuid(self, uuid: str):
        return SqliteJobRepository._to_job(JobDao.find_job_by_uuid(uuid))

    @staticmethod
    def _to_dto(job: Job):
        return JobDto(uuid=job.uuid, name=job.name, url=job.url)

    @staticmethod
    def _to_job(job_dto: JobDto):
        return Job(uuid=job_dto.uuid, name=job_dto.name, url=job_dto.url)


@Repository(name="run_repository")
class SqliteRunRepository(RunRepository):

    def save(self, run: Run) -> Run:
        raise NotImplementedError()

    def delete_by_uuid(self, uuid: str) -> None:
        raise NotImplementedError()

    def find_by_uuid(self, uuid: str) -> Run:
        raise NotImplementedError()
