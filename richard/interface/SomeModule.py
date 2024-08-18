from abc import ABC, abstractmethod

from richard.entity.Relation import Relation


class SomeModule(ABC):

    relations: dict


    def get_relations(self) -> dict[str, Relation]:
        return self.relations

