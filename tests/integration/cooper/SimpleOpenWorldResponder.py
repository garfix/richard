from richard.core.Model import Model
from richard.core.Solver import Solver
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.entity.Variable import Variable
from richard.interface.SomeSolver import SomeSolver
from richard.interface.SomeProcessor import SomeProcessor
from richard.processor.responder.SimpleResponderProduct import SimpleResponderProduct
from richard.processor.semantic_executor.AtomExecutorProduct import AtomExecutorProduct


class SimpleOpenWorldResponder(SomeProcessor):
    """
    Formats the executor's bindings into a formatted response
    """

    model: Model
    executor: SomeProcessor


    def __init__(self, model: Model, executor: SomeProcessor) -> None:
        super().__init__()
        self.model = model
        self.executor = executor


    def get_name(self) -> str:
        return "Responder"


    def process(self, request: SentenceRequest) -> ProcessResult:
        incoming: AtomExecutorProduct = request.get_current_product(self.executor)
        solver = Solver(self.model)
        response = self.create_response(incoming.bindings, solver)
        product = SimpleResponderProduct(response)
        return ProcessResult([product], "")


    def create_response(self, bindings: list[dict], solver: SomeSolver) -> str:

        response = ""

        format = solver.solve1([('format', Variable('Type'))])
        if format == None:
            raise Exception("The sentence doesn't have a 'format' inference")

        type = format["Type"]

        if type == "y/n/u":

            ynu_format = solver.solve1([('format_ynu', Variable('Answer'))])
            if ynu_format == None:
                raise Exception("The sentence doesn't have a 'format_ynu' inference")

            answer_variable = ynu_format["Answer"]

            if len(bindings) != 1:
                results = [binding[answer_variable] for binding in bindings]
                raise Exception("The y/n/u format requires a single result. Got: " + ", ".join(results))

            answer = bindings[0][answer_variable]

            if answer == "true":
                response = "True"
            elif answer == "false":
                response = "False"
            elif answer == "unknown":
                response = "Unable to answer"
            else:
                raise Exception("Unrecognized response: " + str(answer))

        else:
            raise Exception("Unrecognized format type: " + type)

        return response
