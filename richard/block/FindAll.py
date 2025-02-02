from richard.entity.BlockResult import BlockResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.entity.ControlBlock import ControlBlock


class FindAll(ControlBlock):
    """
    This block goes through all alternative products even after one was found that gives no error.
    If no product could be found, however, the first error is returned.
    """

    def process(self, request: SentenceRequest) -> BlockResult:
        result = request.exec_process(self.processor)
        if result.error_type != '':
            return BlockResult(result.error_type, result.error_args)

        error_type = ""
        error_args = []

        # the essence of this block: collect all products
        request.set_alternative_products(self.processor,
            request.get_alternative_products(self.processor) + result.products)

        success = False
        for product in result.products:

            request.set_current_product(self.processor, product)

            next_block_result = self.next_block.process(request)
            success = success or next_block_result.error_type == ""
            if next_block_result.error_type != "" and error_type == "":
                error_type = next_block_result.error_type
                error_args = next_block_result.error_args

        if success:
            return BlockResult("")
        else:
            return BlockResult(error_type, error_args)

