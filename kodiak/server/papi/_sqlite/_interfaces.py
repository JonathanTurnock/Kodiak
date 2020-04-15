from abc import ABC, abstractmethod


class Dto(ABC):

    @abstractmethod
    def parameterize(self) -> dict:
        pass
