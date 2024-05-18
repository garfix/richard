from richard.entity.ParseTreeNode import ParseTreeNode
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeProcessor import SomeProcessor
from richard.interface.SomeSemanticComposer import SomeSemanticComposer


class SemanticExecutor(SomeProcessor):
    """
    Executes the function that forms the meaning of the sentence, and produces its result
    """
    
    composer: SomeSemanticComposer


    def __init__(self, composer: SomeSemanticComposer) -> None:
        super().__init__()
        self.composer = composer    

    
    def process(self, request: SentenceRequest) -> ProcessResult:
        semantic_function = self.composer.get_semantic_function(request)
        results = [semantic_function()]
        return ProcessResult(results, "", [])


    def get_results(self, request: SentenceRequest) -> list:
        return request.get_current_product(self)
