from abc import ABC, abstractmethod
from richard.entity.SentenceRequest import SentenceRequest


class SomeSystem(ABC):
    @abstractmethod
    def enter(self, request: SentenceRequest):
        pass

    @abstractmethod
    def read_output(self):
        pass
