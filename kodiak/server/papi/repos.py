from abc import ABC, abstractmethod
from typing import List

from kodiak.model.job import Job
from kodiak.model.run import Run


class JobRepository(ABC):

    @abstractmethod
    def save(self, job: Job) -> Job:
        pass

    @abstractmethod
    def delete_by_uuid(self, uuid: str) -> None:
        pass

    @abstractmethod
    def find_all(self) -> List[Job]:
        pass

    @abstractmethod
    def find_by_uuid(self, id: int) -> Job:
        pass


class RunRepository(ABC):

    @abstractmethod
    def save(self, run: Run) -> Run:
        pass

    @abstractmethod
    def delete_by_uuid(self, uuid: str) -> None:
        pass
    
    @abstractmethod
    def find_by_uuid(self, uuid: str) -> Run:
        pass
