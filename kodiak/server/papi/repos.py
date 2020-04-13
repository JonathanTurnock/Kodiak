from abc import ABC, abstractmethod
from typing import List

from kodiak.model.job import Job
from kodiak.model.run import Run, Step, Command


class JobRepository(ABC):

    @abstractmethod
    def save(self, job: Job) -> Job:
        pass

    @abstractmethod
    def find_all(self) -> List[Job]:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Job:
        pass


class RunRepository(ABC):

    @abstractmethod
    def save(self, run: Run) -> Run:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Run:
        pass

    @abstractmethod
    def find_by_uuid(self, uuid: str) -> Run:
        pass


class StepRepository(ABC):

    @abstractmethod
    def save(self, step: Step) -> Step:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Step:
        pass

    @abstractmethod
    def find_all_by_run_id(self, run_id: int) -> List[Step]:
        pass


class CommandRepository(ABC):

    @abstractmethod
    def save(self, command: Command) -> Command:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Command:
        pass

    @abstractmethod
    def find_all_by_step_id(self, step_id: int) -> List[Command]:
        pass
