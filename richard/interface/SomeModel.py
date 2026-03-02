from abc import ABC, abstractmethod

from richard.entity.Relation import Relation

class SomeModel(ABC):
    """
    This class represents the generic part of the model.
    """

    @abstractmethod
    def find_relations(self, predicate: str) -> list[Relation]:
        pass

