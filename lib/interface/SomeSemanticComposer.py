from abc import abstractmethod

from lib.entity.SentenceRequest import SentenceRequest
from lib.interface.SomeProcessor import SomeProcessor


class SomeSemanticComposer(SomeProcessor):
    @abstractmethod
    def get_semantic_function(self, request: SentenceRequest) -> callable: 
        pass
