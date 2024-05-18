from richard.entity.BlockResult import BlockResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.entity.ControlBlock import ControlBlock


class TryFirst(ControlBlock):
    """
    This block just tries the first of the alternative products. If it failes, no other products are tried.
    """
    

    def process(self, request: SentenceRequest) -> BlockResult:
        result = self.processor.process(request)
        if result.error_code != '':
            return BlockResult(result.error_code, result.error_args)

        request.set_alternative_products(self.processor, result.products)

        error_code = ""
        error_args = []

        for product in result.products:

            request.set_current_product(self.processor, product)
          
            next_block_result = self.next_block.process(request)
            error_code = next_block_result.error_code
            error_args = next_block_result.error_args

            # first product tried: quit
            break

        return BlockResult(error_code, error_args)

    