from lib.entity.ParseTreeNode import ParseTreeNode
from lib.entity.SentenceRequest import SentenceRequest
from lib.interface.Processor import Processor


class SemanticExecutor(Processor):
    """
    Executes the function that forms the meaning of the sentence, and produces its result
    """
    parser: Processor


    def __init__(self, parser: Processor) -> None:
        super().__init__()
        self.parser = parser    

    
    def process(self, request: SentenceRequest):
        root_node = request.get_current_product(self.parser)
        semantic_function = root_node.rule.sem
        results = semantic_function(root_node)
        return results
