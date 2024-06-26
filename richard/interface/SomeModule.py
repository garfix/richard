from abc import ABC, abstractmethod

from richard.interface import SomeSolver


class SomeModule(ABC):
    @abstractmethod
    def interpret_relation(self, relation_name: str, db_values: list, in_types: list[str], solver: SomeSolver, binding: dict) -> list[list]:
        pass
    
    
    @abstractmethod
    def get_relations(self) -> list[str]:
        pass
