from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeResponseHandler import SomeResponseHandler
from richard.interface.SomeSemanticComposer import SomeSemanticComposer
from richard.interface.SomeSemanticExecutor import SomeSemanticExecutor
from richard.interface.SomeProcessor import SomeProcessor
from richard.type.OrderedSet import OrderedSet


class SimpleResponder(SomeProcessor):
    """
    Formats the executor's bindings into a formatted response
    """
    
    composer: SomeSemanticComposer
    executor: SomeSemanticExecutor
    handler: SomeResponseHandler


    def __init__(self, composer: SomeSemanticComposer, executor: SomeSemanticExecutor, handler: SomeResponseHandler) -> None:
        super().__init__()
        self.composer = composer
        self.executor = executor    
        self.handler = handler

    
    def process(self, request: SentenceRequest) -> ProcessResult:
        bindings = self.executor.get_results(request)
        composition = self.composer.get_composition(request)
        response = self.handler.create_response(bindings, composition)
        return ProcessResult([response], "", [])
    

    def get_response(self, request: SentenceRequest) -> str:
        return request.get_current_product(self)
