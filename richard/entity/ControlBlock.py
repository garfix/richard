from __future__ import annotations
from richard.entity.BlockResult import BlockResult
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeProcessor import SomeProcessor


class ControlBlock:

    processor: SomeProcessor
    next_block: ControlBlock


    def __init__(self, processor) -> None:
        self.processor = processor
    

    def process(self, request: SentenceRequest) -> BlockResult:
        pass

    