from abc import abstractmethod

from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeProcessor import SomeProcessor


class SomeSemanticComposer(SomeProcessor):
    @abstractmethod
    def get_semantic_function(self, request: SentenceRequest) -> callable: 
        pass
