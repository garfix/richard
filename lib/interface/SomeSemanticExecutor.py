from abc import abstractmethod

from lib.entity.SentenceRequest import SentenceRequest
from lib.interface.SomeProcessor import SomeProcessor

class SomeSemanticExecutor(SomeProcessor):
    @abstractmethod
    def get_results(self, request: SentenceRequest) -> list: 
        pass
