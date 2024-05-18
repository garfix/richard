from richard.constants import NO_RESULTS
from richard.entity.BlockResult import BlockResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.entity.Block import Block


class FirstSuccess(Block):
    """
    Returns the product of the first successful successor block.
    No successful blocks? Returns the error of the first failing successor block.
    """

    def process(self, request: SentenceRequest) -> BlockResult:
        product = self.processor.process(request)
        if product.error_code != '':
            return BlockResult([], product.error_code, product.error_args)

        error_code = ""
        error_args = []

        for product in product.products:

            request.set_current_product(self.processor, product)

            self.accepted_products = [product]
            
            if self.next_block:
                next_block_result = self.next_block.process(request)
                success = next_block_result.successful()
                if not success and error_code == "":
                    error_code = next_block_result.error_code
                    error_args = next_block_result.error_args

            else:
                success = True

            if success:
                return BlockResult([product], '', [])
            
        if error_code == "":
            error_code = NO_RESULTS

        return BlockResult([], error_code, error_args)

    
    def get_result(self) -> any:
        pass
