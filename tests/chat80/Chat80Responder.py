from richard.entity.Instance import Instance
from richard.interface.SomeResponseHandler import SomeResponseHandler
from richard.entity.Composition import Composition


class Chat80Responder(SomeResponseHandler):
    def create_response(self, bindings: list[dict], composition: Composition) -> str:
        response = ""
        sep = ""

        if "y/n" in composition.intents:
            if len(bindings) > 0:
                response = "yes"
            else:
                response = "no"
        elif "number" in composition.intents:
            if len(bindings) > 0:
                response = bindings[0]['S1']
            else:
                response = "I dont't know"
        elif "table" in composition.intents:
            response = []
            for binding in bindings:
                # todo: make this more general
                v1 = composition.intents[1]
                v2 = composition.intents[2]
                val1 = binding[v1].id if isinstance(binding[v1], Instance) else binding[v1]
                val2 = binding[v2].id if isinstance(binding[v2], Instance) else binding[v2]
                response.append([val1, val2])
        else:
            s = set()
            for binding in bindings:
                value = binding["S1"].id if isinstance(binding["S1"], Instance) else binding["S1"]
                if value in s:
                    continue
                s.add(value)
                response += sep + value
                sep = ", "

        return response
    