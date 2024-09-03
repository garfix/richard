from richard.core.Logger import Logger
from richard.core.Model import Model
from richard.core.Solver import Solver
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface import SomeResponseHandler
from richard.interface.SomeProcessor import SomeProcessor
from richard.processor.responder.SimpleResponderProduct import SimpleResponderProduct
from richard.processor.semantic_executor.AtomExecutorProduct import AtomExecutorProduct


class SimpleResponder(SomeProcessor):
    """
    Formats the executor's bindings into a formatted response
    """

    model: Model
    executor: SomeProcessor
    handler: SomeResponseHandler


    def __init__(self, model: Model, executor: SomeProcessor, handler: SomeResponseHandler) -> None:
        super().__init__()
        self.model = model
        self.executor = executor
        self.handler = handler


    def get_name(self) -> str:
        return "Responder"


    def process(self, request: SentenceRequest) -> ProcessResult:
        incoming: AtomExecutorProduct = request.get_current_product(self.executor)
        solver = Solver(self.model)
        response = self.handler.create_response(incoming.bindings, solver)
        product = SimpleResponderProduct(response)
        return ProcessResult([product], "")

