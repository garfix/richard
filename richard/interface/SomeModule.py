from abc import ABC, abstractmethod

from richard.entity.Instance import Instance
from richard.interface import SomeSolver


class SomeModule(ABC):
    @abstractmethod
    def get_relations(self) -> list[str]:
        pass

        
    @abstractmethod
    def interpret_relation(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:
        pass
    
    
    def dehydrate_values(self, values: list) -> list:
        dehydrated = []
        for value in values:
            if isinstance(value, Instance):
                dehydrated.append(value.id)
            else:
                dehydrated.append(value)
        return dehydrated


    def hydrate_values(self, rows: list[list], types: list[str]) -> list:
        hydrated = []
        for values in rows:
            new_row = []
            for value, type in zip(values, types):
                if type is not None:
                    new_row.append(Instance(type, value))
                else:
                    new_row.append(value)
            hydrated.append(new_row)
        return hydrated
