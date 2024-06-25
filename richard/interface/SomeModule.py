from abc import ABC, abstractmethod

from richard.interface import SomeSolver


class SomeModule(ABC):
    @abstractmethod
    def interpret_relation(self, relation_name: str, values: list, solver: SomeSolver) -> list[list]:
        pass
    