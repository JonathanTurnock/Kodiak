from fxq.core.stereotype import Repository

from fxq.ae.runner.model import Executor


@Repository
class ExecutorRepository:

    sequence: int = 0

    def __init__(self):
        self._executors = []

    def save(self, executor: Executor) -> Executor:
        ExecutorRepository.sequence += 1
        executor.id = ExecutorRepository.sequence
        self._executors.append(executor)
        return executor

    def find_all(self):
        return self._executors
