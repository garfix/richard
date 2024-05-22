from dataclasses import dataclass

from richard.entity.Relation import Relation
from richard.entity.Entity import Entity
from richard.semantics.commands import dnp


class Model:
    """
    This class represents the state of the world, and is the source of truth for the pipeline
    """

    entities: dict[str, Entity]
    relations: dict[str, Relation]
    select: callable


    def __init__(self, entities: list[Entity], relations: list[Relation], select: callable) -> None:
        self.entities = {}
        for type in entities:
            self.entities[type.name] = type

        self.relations = {}
        for relation in relations:
            self.relations[relation.name] = relation

        self.select = select


    def get_entity_ids(self, type_name: str):
        if not type_name in self.entities:
            raise Exception('No type ' + type_name + " in domain")
        
        type = self.entities[type_name]
        return type.get_all_ids()


    def relation_exists(self, relation_name: str, field_values: list[any]):
        if not relation_name in self.relations:
            raise Exception('No relation ' + relation_name + " in domain")
          
        relation = self.relations[relation_name]
        return self.select(relation, field_values)

    def search_first(self, relation_name: str, dnp: dnp):
        if not relation_name in self.relations:
            raise Exception('No relation ' + relation_name + " in domain")

        elements = dnp.nbar()
        relation = self.relations[relation_name]
        results = []
        for e in elements:
            values = [None, e]
            for f in self.select(relation, values):
                results.append(f[0])

        if dnp.determiner(len(results), len(elements)):
            return results
        else:
            return []
