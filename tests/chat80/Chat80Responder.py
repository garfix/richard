from richard.entity.Instance import Instance
from richard.interface.SomeResponseHandler import SomeResponseHandler
from richard.entity.Composition import Composition


class Chat80Responder(SomeResponseHandler):
    def create_response(self, bindings: list[dict], composition: Composition) -> str:
        response = ""

        format = None
        type = None
        for atom in composition.inferences:
            if atom[0] == 'format':
                format = atom
                type = format[1]

        if type == "y/n":
            if len(bindings) > 0:
                response = "yes"
            else:
                response = "no"

        elif type == "number":
            variable = format[2]
            unit = format[3]
            
            v = variable.name
            if len(bindings) > 0:
                response = bindings[0][v]
                if unit:
                    response = str(response) + " " + unit
            else:
                response = "I dont't know"

        elif type == "table":
            columns = format[2]
            units = format[3]

            response = []
            for binding in bindings:

                row = []
                for variable, unit in zip(columns, units):
                    v = variable.name
                    value = binding[v].id if isinstance(binding[v], Instance) else binding[v]
                    if isinstance(value, float):
                        value = str(int(value))
                    if unit:
                        value = str(value) + " " + unit
                    row.append(value)
                response.append(row)

            response = sorted(response, key = lambda row: row[0])

        elif type == "list":
            variable = format[2]
            v = variable.name
            s = set()
            values = []
            for binding in bindings:
                value = binding[v].id if isinstance(binding[v], Instance) else binding[v]
                if value in s:
                    continue
                s.add(value)
                values.append(value)
            values.sort()
            response = ", ".join(values)

        else:
            raise Exception("The sentence doesn't have a 'format' inference")

        return response
    