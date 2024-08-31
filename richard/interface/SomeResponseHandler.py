from abc import abstractmethod

from richard.interface.SomeSolver import SomeSolver

class SomeResponseHandler:
    @abstractmethod
    def create_response(self, bindings: list[dict], solver: SomeSolver) -> str:
        pass
