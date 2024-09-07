from richard.entity.Variable import Variable
from richard.interface.SomeSolver import SomeSolver
from richard.interface.SomeResponseHandler import SomeResponseHandler


class WikidataResponder(SomeResponseHandler):
    def create_response(self, bindings: list[dict], solver: SomeSolver) -> str:

        formats = solver.solve([('format', Variable('Type'), Variable('Variable'))])
        if len(formats) == 0:
            raise Exception("The sentence doesn't have a 'format' inference")

        type = formats[0]["Type"]
        variable = formats[0]["Variable"]
        response = ""

        if type == "list":
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

        else:
            raise Exception("Unrecognized format type: " + type)

        return response
