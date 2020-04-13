from typing import List

from fxq.core.beans.factory.annotation import Autowired
from fxq.core.stereotype import Repository

from kodiak.model.job import Job
from kodiak.model.run import Run, Command, Step, Status
from kodiak.server.papi._sqlite.command import command_dto_of_command, CommandDao, CommandDto
from kodiak.server.papi._sqlite.job import JobDto, JobDao
from kodiak.server.papi._sqlite.run import RunDto, run_dto_of_run, RunDao
from kodiak.server.papi._sqlite.schema import SchemaInterface
from kodiak.server.papi._sqlite.step import step_dto_of_step, StepDao, StepDto
from kodiak.server.papi.repos import JobRepository, RunRepository, StepRepository, CommandRepository

schema_interface: SchemaInterface = Autowired("schema_interface")
schema_interface.check_for_updates()


@Repository(name="job_repository")
class SqliteJobRepository(JobRepository):

    def save(self, job: Job) -> Job:
        job_dto = JobDto(
            id=job.id,
            name=job.name,
            url=job.url
        )
        job_dto: JobDto = JobDao.save(job_dto)
        if job.id is None:
            job.id = job_dto.id
        return job

    def find_all(self) -> List[Job]:
        return [Job(
            id=job_dto.id,
            name=job_dto.name,
            url=job_dto.url
        ) for job_dto in JobDao.find_jobs()]

    def find_by_id(self, id: int):
        job_dto = JobDao.find_job_by_id(id)
        job = Job(
            id=job_dto.id,
            name=job_dto.name,
            url=job_dto.url
        )
        return job


@Repository(name="run_repository")
class SqliteRunRepository(RunRepository):

    def save(self, run: Run) -> Run:
        run_dto = run_dto_of_run(run)
        run_dto: RunDto = RunDao.save(run_dto)
        if run.id is None:
            run.id = run_dto.id
        return run

    def find_by_id(self, id: int) -> Run:
        run_dto: RunDto = RunDao.find_by_id(id)
        job_dto: JobDto = JobDao.find_job_by_id(run_dto.job_id)
        job = Job(
            id=job_dto.id,
            name=job_dto.name,
            url=job_dto.url
        )
        run = Run(
            id=run_dto.id,
            job=job,
            uuid=run_dto.uuid,
            status=Status.value_of(run_dto.status),
            started=run_dto.started,
            ended=run_dto.ended,
        )
        return run

    def find_by_uuid(self, uuid: str) -> Run:
        run_dto: RunDto = RunDao.find_by_uuid(uuid)
        job_dto: JobDto = JobDao.find_job_by_id(run_dto.job_id)
        job = Job(
            id=job_dto.id,
            name=job_dto.name,
            url=job_dto.url
        )
        run = Run(
            id=run_dto.id,
            job=job,
            uuid=run_dto.uuid,
            status=Status.value_of(run_dto.status),
            started=run_dto.started,
            ended=run_dto.ended,
        )
        return run


@Repository(name="step_repository")
class SqliteStepRepository(StepRepository):

    def __init__(self, run_repository=Autowired("run_repository")):
        self._run_repository = run_repository

    def save(self, step: Step) -> Step:
        step_dto = step_dto_of_step(step)
        step_dto: StepDto = StepDao.save(step_dto)
        if step.id is None:
            step.id = step_dto.id
        return step

    def find_by_id(self, id: int) -> Step:
        dto = StepDao.find_by_id(id)
        run = self._run_repository.find_by_id(dto.run_id)
        return Step(
            id=dto.id,
            run=run,
            number=dto.number,
            name=dto.name,
            image=dto.image,
            status=Status.value_of(dto.status)
        )

    def find_all_by_run_id(self, run_id: int) -> List[Step]:
        run = self._run_repository.find_by_id(run_id)
        return [Step(
            id=dto.id,
            run=run,
            number=dto.number,
            name=dto.name,
            image=dto.image,
            status=Status.value_of(dto.status)

        ) for dto in StepDao.find_all_by_run_id(run_id)]


@Repository(name="command_repository")
class SqliteCommandRepository(CommandRepository):

    def __init__(self, step_repository=Autowired("step_repository")):
        self._step_repository = step_repository

    def save(self, command: Command) -> Command:
        command_dto = command_dto_of_command(command)
        command_dto: CommandDto = CommandDao.save(command_dto)
        if command.id is None:
            command.id = command_dto.id
        return command

    def find_by_id(self, id: int) -> Command:
        dto = CommandDao.find_by_id(id)
        step = self._step_repository.find_by_id(dto.step_id)
        return Command(
            id=dto.id,
            step=step,
            number=dto.number,
            instruction=dto.instruction,
            std_out=dto.std_out,
            std_err=dto.std_err
        )

    def find_all_by_step_id(self, step_id: int) -> List[Command]:
        step = self._step_repository.find_by_id(step_id)
        return [Command(
            id=dto.id,
            step=step,
            number=dto.number,
            instruction=dto.instruction,
            std_out=dto.std_out,
            std_err=dto.std_err
        ) for dto in CommandDao.find_all_by_step_id(step_id)]
