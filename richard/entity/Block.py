from __future__ import annotations
from richard.entity.BlockResult import BlockResult
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeProcessor import SomeProcessor


class Block:

    processor: SomeProcessor
    next_block: Block

    # results of the latest process
    # _current_results: list[ProcessResult]

    # the output of the block
    # accepted_products: list[ProcessResult]


    def __init__(self, processor) -> None:
        self.processor = processor
        # self._current_results = []
        # self.accepted_products = []


    def process(self, request: SentenceRequest) -> BlockResult:
        pass

    
    def get_result(self) -> any:
        pass
