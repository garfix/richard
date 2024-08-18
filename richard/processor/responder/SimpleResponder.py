from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeSolver import SomeSolver
from richard.interface.SomeResponseHandler import SomeResponseHandler
from richard.interface.SomeSemanticComposer import SomeSemanticComposer
from richard.interface.SomeSemanticExecutor import SomeSemanticExecutor
from richard.interface.SomeProcessor import SomeProcessor


class SimpleResponder(SomeProcessor):
    """
    Formats the executor's bindings into a formatted response
    """
    
    solver: SomeSolver
    executor: SomeSemanticExecutor
    handler: SomeResponseHandler


    def __init__(self, solver: SomeSolver, executor: SomeSemanticExecutor, handler: SomeResponseHandler) -> None:
        super().__init__()
        self.solver = solver
        self.executor = executor    
        self.handler = handler

    
    def process(self, request: SentenceRequest) -> ProcessResult:
        bindings = self.executor.get_results(request)
        response = self.handler.create_response(bindings, self.solver)
        return ProcessResult([response], "")
    

    def get_response(self, request: SentenceRequest) -> str:
        return request.get_current_product(self)
