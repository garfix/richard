from richard.Model import Model
from richard.entity.ParseTreeNode import ParseTreeNode
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeProcessor import SomeProcessor
from richard.interface.SomeSemanticComposer import SomeSemanticComposer
from richard.type.OrderedSet import OrderedSet


class TupleExecutor(SomeProcessor):
    """
    Executes the function that forms the meaning of the sentence, and produces its result
    """
    
    composer: SomeSemanticComposer
    model: Model


    def __init__(self, composer: SomeSemanticComposer, model: Model) -> None:
        super().__init__()
        self.composer = composer    
        self.model = model

    
    def process(self, request: SentenceRequest) -> ProcessResult:
        sentence_tuples = self.composer.get_tuples(request)
        tuples = sentence_tuples()
        bindngs = self.collect(tuples)
        
        return ProcessResult(tuples, "", [])
    

    def collect(self, tuples: list[tuple]) -> OrderedSet[dict]:
        pass


    def get_results(self, request: SentenceRequest) -> list:
        return request.get_current_product(self)
