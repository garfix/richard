from richard.block.Succeed import Succeed
from richard.core.Model import Model
from richard.core.Solver import Solver
from richard.entity.ControlBlock import ControlBlock
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeClearableDb import SomeClearableDb
from richard.interface.SomeGenerator import SomeGenerator


class System:
    """
    This class contains all blocks/processors involved in the processing of a sentence.
    The number and type of blocks and processors depend on the purpose of the application.
    When a new sentence request comes in, it is sent through the blocks.
    Each processor generates one or more alternative interpretations (ambiguity), and the pipeline processes these one by one.
    Each processor has access to the active alternative interpretations of its predecessors.
    """

    reader_pipeline: list[ControlBlock]
    output_generator: SomeGenerator
    model: Model

    def __init__(self, model: Model=None, input_pipeline: list[ControlBlock]=[], output_generator: SomeGenerator=None):

        self.model = model
        self.reader_pipeline = input_pipeline
        self.output_generator = output_generator

        # this blocks is added last, so that the other blocks don't need to check if there's a next one
        terminal = Succeed(None)

        # link each block to the next
        for i, block in enumerate(self.reader_pipeline):
            block.next_block = self.reader_pipeline[i+1] if i < len(self.reader_pipeline)-1 else terminal


    def enter(self, request: SentenceRequest):

        result = self.reader_pipeline[0].process(request)
        if result.error_type != "":
            Solver(self.model).solve([('store', [
                ('output_type', result.error_type),
                ('output_' + result.error_type, *result.error_args)])])
        else:
            # go to the last processor
            processor = self.reader_pipeline[-1].processor
            # get the product
            product = request.get_current_product(processor)
            # return its output value
            return product.get_output()


    def read_output(self):
        return self.output_generator.generate_output()
