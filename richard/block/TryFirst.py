from richard.entity.BlockResult import BlockResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.entity.ControlBlock import ControlBlock


class TryFirst(ControlBlock):
    """
    This block just tries the first of the alternative products. If it failes, no other products are tried.
    """


    def process(self, request: SentenceRequest) -> BlockResult:
        result = request.log_process(self.processor)
        if result.error != '':
            return BlockResult(result.error)

        request.set_alternative_products(self.processor, result.products)

        error = ""

        for product in result.products:

            request.set_current_product(self.processor, product)

            next_block_result = self.next_block.process(request)
            error = next_block_result.error

            # first product tried: quit
            break

        return BlockResult(error)

