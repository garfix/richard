from richard.entity.BlockResult import BlockResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.entity.ControlBlock import ControlBlock


class FindOne(ControlBlock):
    """
    This block goes through all alternative products until it finds one that gives no error.
    If no such product could be found, the first error is returned.
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
            if next_block_result.error_type == "":
               # first successful product found: quit
               return BlockResult('')
            else:
                error_type = next_block_result.error_type
                error_args = next_block_result.error_args

        return BlockResult(error_type, error_args)

