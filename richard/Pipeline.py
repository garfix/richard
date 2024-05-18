from dataclasses import dataclass

from richard.entity.BlockResult import BlockResult
from richard.entity.Block import Block
from richard.entity.SentenceRequest import SentenceRequest


@dataclass(frozen=True)
class Pipeline:
    """
    This class contains all processors involved in the processing of a sentence.
    The number and type of processors depend on the purpose of the application.
    When a new sentence comes in, it creates a request for it ans sends it trough the pipeline of processors.
    Each processor generates one or more alternative interpretations (ambiguity), and the pipeline processes these one by one.
    Each processor has access to the active alternative interpretations of its predecessors.
    """
    
    blocks: list[Block]
    block_index: int = -1

    def __post_init__(self):
        for i, block in enumerate(self.blocks):
            next_block = self.blocks[i+1] if i < len(self.blocks)-1 else None
            block.next_block = next_block


    def enter(self, request: SentenceRequest) -> BlockResult:
        return self.blocks[0].process(request)

