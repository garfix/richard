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
        else:
            for binding in bindings:
                response += sep + str(binding["S1"].id)
                sep = ", "

        return response
    