from richard.constants import NO_RESULTS
from richard.entity.BlockResult import BlockResult
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.entity.Block import Block


class FindAll(Block):

    def process(self, request: SentenceRequest) -> BlockResult:
        product = self.processor.process(request)
        if product.error_code != '':
            return BlockResult([], product.error_code, product.error_args)

        error_code = ""
        error_args = []

        request.set_alternative_products(self.processor, 
            request.get_alternative_products(self.processor) + product.products)

        for product in product.products:

            request.set_current_product(self.processor, product)


            self.accepted_products = [product]
            
            if self.next_block:
                next_block_result = self.next_block.process(request)
                success = next_block_result.successful()
            else:
                success = True
           
        return BlockResult([], error_code, error_args)
    

    def get_result(self) -> any:
        pass

