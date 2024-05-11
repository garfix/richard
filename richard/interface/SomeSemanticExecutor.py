from abc import abstractmethod

from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeProcessor import SomeProcessor

class SomeSemanticExecutor(SomeProcessor):
    @abstractmethod
    def get_results(self, request: SentenceRequest) -> list: 
        pass
