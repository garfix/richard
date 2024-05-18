from richard.constants import NO_RESULTS
from richard.entity.BlockResult import BlockResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.entity.ControlBlock import ControlBlock


class FindAll(ControlBlock):
    """
    This block goes through all alternative products even after one was found that gives no error.
    If no product could be found, however, the first error is returned.
    """

    def process(self, request: SentenceRequest) -> BlockResult:
        result = self.processor.process(request)
        if result.error_code != '':
            return BlockResult(result.error_code, result.error_args)

        error_code = ""
        error_args = []

        # the essence of this block: collect all products
        request.set_alternative_products(self.processor, 
            request.get_alternative_products(self.processor) + result.products)

        success = False
        for product in result.products:

            request.set_current_product(self.processor, product)

            next_block_result = self.next_block.process(request)
            success = success or next_block_result.error_code == ""
            if next_block_result.error_code != "" and error_code == "":
                error_code = next_block_result.error_code
                error_args = next_block_result.error_args
           
        if success:
            return BlockResult("", [])    
        else:
            return BlockResult(error_code, error_args)
    
