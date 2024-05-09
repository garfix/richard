from lib.entity.ParseTreeNode import ParseTreeNode
from lib.entity.SentenceRequest import SentenceRequest
from lib.interface.Processor import Processor


class SemanticExecutor(Processor):
    """
    Executes the function that forms the meaning of the sentence, and produces its result
    """
    composer: Processor


    def __init__(self, composer: Processor) -> None:
        super().__init__()
        self.composer = composer    

    
    def process(self, request: SentenceRequest):
        semantic_function = request.get_current_product(self.composer)
        print('START EXECUTION')
        results = semantic_function()
        return results
