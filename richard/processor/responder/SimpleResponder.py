from richard.core.Model import Model
from richard.core.Solver import Solver
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.entity.Variable import Variable
from richard.interface.SomeSolver import SomeSolver
from richard.interface.SomeProcessor import SomeProcessor
from richard.processor.responder.SimpleResponderProduct import SimpleResponderProduct
from richard.processor.semantic_executor.AtomExecutorProduct import AtomExecutorProduct


class SimpleResponder(SomeProcessor):
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

        if type == "y/n":

            if len(bindings) > 0:
                response = "yes"
            else:
                response = "no"

        elif type == "number":

            number_format = solver.solve1([('format_number', Variable('Variable'), Variable('Unit'))])
            if number_format == None:
                raise Exception("The sentence doesn't have a 'format_number' inference")

            variable = number_format["Variable"]
            unit = number_format["Unit"]

            if len(bindings) > 0:
                response = bindings[0][variable]
                if unit:
                    response = str(response) + " " + unit

            canned = solver.solve1([('format_canned', Variable('Template'))])
            if canned != None:
                response = canned['Template'].replace('{}', str(response))

            else:
                response = "I dont't know"

        elif type == "table":

            table_format = solver.solve1([('format_table', Variable('Variables'), Variable('Units'))])
            if table_format == None:
                raise Exception("The sentence doesn't have a 'format_table' inference")

            variables = table_format["Variables"]
            units = table_format["Units"]

            response = []
            for binding in bindings:

                row = []
                for variable, unit in zip(variables, units):
                    value = binding[variable]
                    if isinstance(value, float):
                        value = str(int(value))
                    if unit:
                        value = str(value) + " " + unit
                    row.append(value)
                response.append(row)

            response = sorted(response, key = lambda row: row[0])

        elif type == "list":

            list_format = solver.solve1([('format_list', Variable('Variable'))])
            if list_format == None:
                raise Exception("The sentence doesn't have a 'format_list' inference")

            variable = list_format["Variable"]

            s = set()
            values = []
            for binding in bindings:
                value = binding[variable]
                if value in s:
                    continue
                s.add(value)
                values.append(value)
            values.sort()
            response = ", ".join(values)

            canned = solver.solve1([('format_canned', Variable('Template'))])
            if canned != None:
                response = canned['Template'].replace('{}', str(response))

        elif type == "canned":

            canned_format = solver.solve1([('format_canned', Variable('Response'))])
            if canned_format == None:
                raise Exception("The sentence doesn't have a 'format_canned' inference")

            response = canned_format["Response"]

        else:
            raise Exception("Unrecognized format type: " + type)

        return response
