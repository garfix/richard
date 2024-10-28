from abc import ABC, abstractmethod

from richard.entity.Relation import Relation


class SomeModule(ABC):

    relations: dict


    def __init__(self) -> None:
        self.relations = {}


    def add_relation(self, relation: Relation):
        self.relations[relation.predicate] = relation


    def get_relations(self) -> dict[str, Relation]:
        return self.relations

