from abc import ABC, abstractmethod

from richard.entity.ProcessResult import ProcessResult


"""
Every processor needs to have access to the current alternative interpretation of its predecessor.
To this end it must inject these processors as dependencies. The dependency serves as a key: 
    only with the key can the pipeline be sure that the dependent processor exists.
"""
class SomeProcessor(ABC):
    @abstractmethod
    def process(self, request) -> ProcessResult: # sorry, can't annotate type, because of circular dependency
        pass
