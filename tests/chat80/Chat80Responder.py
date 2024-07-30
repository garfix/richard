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
                response.append([value.id if isinstance(value, Instance) else value for value in binding.values()])
        else:
            for binding in bindings:
                value = binding["S1"].id if isinstance(binding["S1"], Instance) else binding["S1"]
                response += sep + value
                sep = ", "

        return response
    