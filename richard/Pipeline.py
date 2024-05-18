from dataclasses import dataclass

from richard.block.Succeed import Succeed
from richard.entity.BlockResult import BlockResult
from richard.entity.ControlBlock import ControlBlock
from richard.entity.SentenceRequest import SentenceRequest


@dataclass(frozen=True)
class Pipeline:
    """
    This class contains all blocks/processors involved in the processing of a sentence.
    The number and type of blocks and processors depend on the purpose of the application.
    When a new sentence request comes in, it is sent through the blocks.
    Each processor generates one or more alternative interpretations (ambiguity), and the pipeline processes these one by one.
    Each processor has access to the active alternative interpretations of its predecessors.
    """
    
    blocks: list[ControlBlock]
    block_index: int = -1

    def __post_init__(self):
        # this blocks is added last, so that the other blocks don't need to check if there's a next one
        terminal = Succeed(None)
        for i, block in enumerate(self.blocks):
            next_block = self.blocks[i+1] if i < len(self.blocks)-1 else terminal
            block.next_block = next_block


    def enter(self, request: SentenceRequest) -> BlockResult:
        return self.blocks[0].process(request)

