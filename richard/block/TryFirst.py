from richard.entity.BlockResult import BlockResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.entity.ControlBlock import ControlBlock


class TryFirst(ControlBlock):
    """
    This block just tries the first of the alternative products. If it failes, no other products are tried.
    """


    def process(self, request: SentenceRequest) -> BlockResult:
        result = request.exec_process(self.processor)
        if result.error_type != '':
            return BlockResult(result.error_type, result.error_args)

        request.set_alternative_products(self.processor, result.products)

        error_type = ""
        error_args = []

        for product in result.products:

            request.set_current_product(self.processor, product)

            next_block_result = self.next_block.process(request)
            error_type = next_block_result.error_type
            error_args = next_block_result.error_args

            # first product tried: quit
            break

        return BlockResult(error_type, error_args)

