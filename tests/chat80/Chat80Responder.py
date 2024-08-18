from richard.entity.Variable import Variable
from richard.interface.SomeSolver import SomeSolver
from richard.interface.SomeResponseHandler import SomeResponseHandler


class Chat80Responder(SomeResponseHandler):
    def create_response(self, bindings: list[dict], solver: SomeSolver) -> str:

        formats = solver.solve([('format', Variable('Type'), Variable('Variables'), Variable('Units'))])
        if len(formats) == 0:
            raise Exception("The sentence doesn't have a 'format' inference")

        type = formats[0]["Type"]
        variables = formats[0]["Variables"]
        units = formats[0]["Units"]
        response = ""

        if type == "y/n":
            if len(bindings) > 0:
                response = "yes"
            else:
                response = "no"

        elif type == "number":
            variable = variables[0]
            unit = units[0]

            if len(bindings) > 0:
                response = bindings[0][variable]
                if unit:
                    response = str(response) + " " + unit
            else:
                response = "I dont't know"

        elif type == "table":
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
            variable = variables[0]
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
