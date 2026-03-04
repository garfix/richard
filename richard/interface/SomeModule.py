from abc import ABC, abstractmethod

from richard.entity.Relation import Relation


class SomeModule(ABC):

    relations: dict


    def __init__(self) -> None:
        self.relations = {}


    def add_relation(self, relation: Relation):
        self.relations[relation.predicate] = relation


    def get_relation(self, predicate: str) -> Relation|None:
        return self.relations[predicate] if predicate in self.relations else None


