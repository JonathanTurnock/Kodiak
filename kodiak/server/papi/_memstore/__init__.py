import copy
from typing import List

from fxq.core.stereotype import Repository

from kodiak.model.job import Job
from kodiak.model.run import Run
from kodiak.server.papi.exception import NoResultException
from kodiak.server.papi.repos import JobRepository, RunRepository


@Repository(name="job_repository")
class InMemoryJobRepository(JobRepository):

    def __init__(self):
        self._jobs = {}

    def save(self, job: Job) -> Job:
        self._jobs[job.uuid] = job
        return job

    def delete_by_uuid(self, uuid: str) -> None:
        self.find_by_uuid(uuid)
        del self._jobs[uuid]

    def find_all(self) -> List[Job]:
        return [job for job in self._jobs.values()]

    def find_by_uuid(self, uuid: str) -> Job:
        if uuid not in self._jobs.keys():
            raise NoResultException(f"No Job with UUID {uuid}")
        return self._jobs[uuid]


@Repository(name="run_repository")
class InMemoryRunRepository(RunRepository):

    def __init__(self):
        self._runs = {}

    def save(self, run: Run) -> Run:
        self._runs[run.uuid] = copy.deepcopy(run)
        return self._runs[run.uuid]

    def delete_by_uuid(self, uuid: str) -> None:
        self.find_by_uuid(uuid)
        del self._runs[uuid]

    def find_by_uuid(self, uuid: str) -> Run:
        if uuid not in self._runs.keys():
            raise NoResultException(f"No Run with UUID {uuid}")
        return self._runs[uuid]

    def find_all_by_job_uuid(self, uuid: str) -> List[Run]:
        return [run for run in self._runs.values() if run.job.uuid == uuid]
