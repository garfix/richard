from richard.entity.BlockResult import BlockResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.entity.ControlBlock import ControlBlock


class FindOne(ControlBlock):
    """
    This block goes through all alternative products until it finds one that gives no error.
    If no such product could be found, the first error is returned.
    """

    def process(self, request: SentenceRequest) -> BlockResult:
        result = self.processor.wrap_process(request)
        if result.error != '':
            return BlockResult(result.error)

        request.set_alternative_products(self.processor, result.products)

        error = ""

        for product in result.products:

            request.set_current_product(self.processor, product)

            next_block_result = self.next_block.process(request)
            if next_block_result.error == "":
               # first successful product found: quit
               return BlockResult('')
            else:
                error = next_block_result.error

        return BlockResult(error)

