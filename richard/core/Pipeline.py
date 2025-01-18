from richard.block.Succeed import Succeed
from richard.entity.ControlBlock import ControlBlock
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeGenerator import SomeGenerator


class Pipeline:
    """
    This class contains all blocks/processors involved in the processing of a sentence.
    The number and type of blocks and processors depend on the purpose of the application.
    When a new sentence request comes in, it is sent through the blocks.
    Each processor generates one or more alternative interpretations (ambiguity), and the pipeline processes these one by one.
    Each processor has access to the active alternative interpretations of its predecessors.
    """

    blocks: list[ControlBlock]
    generator: SomeGenerator


    def __init__(self, blocks: list[ControlBlock], generator: SomeGenerator = None):

        self.blocks = blocks
        self.generator = generator

        # this blocks is added last, so that the other blocks don't need to check if there's a next one
        terminal = Succeed(None)

        # link each block to the next
        for i, block in enumerate(self.blocks):
            block.next_block = self.blocks[i+1] if i < len(self.blocks)-1 else terminal


    def enter(self, request: SentenceRequest) -> any:

        result = self.blocks[0].process(request)
        if result.error != "":
            return result.error
        else:
            # go to the loas processor
            processor = self.blocks[-1].processor
            # get the product
            product = request.get_current_product(processor)
            # return its output value
            return product.get_output()
