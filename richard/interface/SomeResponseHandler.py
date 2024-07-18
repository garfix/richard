from abc import abstractmethod

from richard.entity.Composition import Composition

class SomeResponseHandler:
    @abstractmethod
    def create_response(self, bindings: list[dict], composition: Composition) -> str:
        pass
