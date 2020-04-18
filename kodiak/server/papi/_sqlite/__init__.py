import logging
import sqlite3
from typing import List

from fxq.core.beans.factory.annotation import Autowired
from fxq.core.stereotype import Repository

from kodiak.model.job import Job
from kodiak.model.run import Run, Status, Step, Command
from kodiak.server.papi._sqlite.command import CommandDao, CommandDto
from kodiak.server.papi._sqlite.job import JobDto, JobDao
from kodiak.server.papi._sqlite.run import RunDto, RunDao
from kodiak.server.papi._sqlite.schema import SchemaInterface
from kodiak.server.papi._sqlite.step import StepDao, StepDto
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
        job: JobDto = JobDao.find_job_by_uuid(uuid)
        JobDao.delete(job)

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
        job_dto = JobDao.find_job_by_uuid(run.job.uuid)
        run_dto = RunDao.save(
            RunDto(job_id=job_dto.id, uuid=run.uuid, status=run.status.name, started=run.started, ended=run.ended))
        for step in run.steps:
            step_dto = StepDao.save(
                StepDto(run_id=run_dto.id, number=step.number, name=step.name, image=step.image,
                        status=step.status.name)
            )
            for command in step.commands:
                command_dto = CommandDao.save(
                    CommandDto(step_id=step_dto.id, number=step_dto.number, instruction=command.instruction,
                               std_out=command.std_out, std_err=command.std_err)
                )
        return run

    def delete_by_uuid(self, uuid: str) -> None:
        run: RunDto = RunDao.find_by_uuid(uuid)
        RunDao.delete(run)

    def find_by_uuid(self, uuid: str) -> Run:
        def get_commands_for_step(step_id: int) -> List[Command]:
            return [Command(number=dto.number, instruction=dto.instruction, std_out=dto.std_out, std_err=dto.std_err)
                    for dto in CommandDao.find_all_by_step_id(step_id)]

        def get_steps_for_run(run_id: int) -> List[Step]:
            return [Step(number=dto.number, name=dto.name, image=dto.image, status=Status(dto.status),
                         commands=get_commands_for_step(dto.id)) for dto in StepDao.find_all_by_run_id(run_id)]

        run_dto: RunDto = RunDao.find_by_uuid(uuid)
        job_dto: JobDto = JobDao.find_job_by_id(run_dto.job_id)

        return Run(
            job=Job(uuid=job_dto.uuid, name=job_dto.name, url=job_dto.url),
            uuid=run_dto.uuid,
            status=Status.value_of(run_dto.status),
            started=run_dto.started,
            ended=run_dto.ended,
            steps=get_steps_for_run(run_dto.id)
        )

    def find_all_by_job_uuid(self, uuid: str) -> List[Run]:
        job_dto: JobDto = JobDao.find_job_by_uuid(uuid)
        run_dtos: List[RunDto] = RunDao.find_all_by_job_id(job_dto.id)
        return [self.find_by_uuid(dto.uuid) for dto in run_dtos]
