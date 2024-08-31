from abc import ABC, abstractmethod

from richard.entity.ProcessResult import ProcessResult
from richard.interface.SomeSentenceRequest import SomeSentenceRequest


"""
Every processor needs to have access to the current alternative interpretation of its predecessor.
To this end it must inject these processors as dependencies. The dependency serves as a key:
    only with the key can the pipeline be sure that the dependent processor exists.
"""
class SomeProcessor(ABC):

    @abstractmethod
    def process(self, request: SomeSentenceRequest) -> ProcessResult:
        pass


    def wrap_process(self, request: SomeSentenceRequest) -> ProcessResult:

        from richard.entity.Logger import ALL, Logger

        result = self.process(request)
        logger: Logger = request.logger

        if logger.is_active() and logger.show_alternatives == ALL:
            if not logger.show_processors or self in logger.show_processors:
                for product in result.products:
                    logger.add(product)

        return result
