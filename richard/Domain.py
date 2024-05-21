from dataclasses import dataclass

from richard.entity.Relation import Relation
from richard.entity.Entity import Entity
from richard.semantics.commands import dnp


class Domain:
    """
    This class represents the state of the world, and is the source of truth for the pipeline
    """

    indexed_entities: dict[str, Entity]
    indexed_relations: dict[str, Relation]
    select: callable


    def __init__(self, entities: list[Entity], relations: list[Relation], select: callable) -> None:
        self.indexed_entities = {}
        for type in entities:
            self.indexed_entities[type.name] = type

        self.indexed_relations = {}
        for relation in relations:
            self.indexed_relations[relation.name] = relation

        self.select = select


    def get_entity_ids(self, type_name: str):
        if not type_name in self.indexed_entities:
            raise Exception('No type ' + type_name + " in domain")
        
        type = self.indexed_entities[type_name]
        return type.get_all_ids()


    def relation_exists(self, type_name: str, field_values: list[any]):
        if not type_name in self.indexed_relations:
            raise Exception('No relation ' + type_name + " in domain")
          
        relation = self.indexed_relations[type_name]
        return self.select(relation, field_values)

    def search(self, relation_name: str, dnp: dnp, value_index: int):
        elements = dnp.nbar()
        relation = self.indexed_relations[relation_name]
        other_index = 0 if value_index == 1 else 0
        results = []
        for e in elements:
            values = [None, None]
            values[value_index] = e
            for f in self.select(relation, values):
                results.append(f[other_index])

        return results
