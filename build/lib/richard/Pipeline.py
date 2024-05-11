from dataclasses import dataclass

from richard.entity.SentenceRequest import SentenceRequest
from .interface.SomeProcessor import SomeProcessor


@dataclass(frozen=True)
class Pipeline:
    """
    This class contains all processors involved in the processing of a sentence.
    The number and type of processors depend on the purpose of the application.
    When a new sentence comes in, it creates a request for it ans sends it trough the pipeline of processors.
    Each processor generates one or more alternative interpretations (ambiguity), and the pipeline processes these one by one.
    Each processor has access to the active alternative interpretations of its predecessors.
    """
    
    processors: list[SomeProcessor]


    def enter(self, request: SentenceRequest):
        self.try_processor(0, request)

    
    def try_processor(self, process_index: int, request: SentenceRequest):
        processor = self.processors[process_index]
        alternatives = processor.process(request)
        request.set_alternative_products(processor, alternatives)
        for alternative in alternatives:
            request.set_current_product(processor, alternative)
            if process_index+1 == len(self.processors):
                return True
            success = self.try_processor(process_index+1, request)
            if success:
                return True
        return False
