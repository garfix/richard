from dataclasses import dataclass

from richard.entity.Range import Range
from richard.entity.Attribute import Attribute
from richard.entity.Modifier import Modifier
from richard.entity.Relation import Relation
from richard.entity.Entity import Entity


class ModelAdapter:
    """
    This class represents the domain-specific part of the model. Extend it to fit your needs.
    """

    modifiers = dict[str, Modifier]
    attributes = dict[str, Attribute]
    entities: dict[str, Entity]
    relations: dict[str, Relation]


    def __init__(
            self, 
            entities: list[Entity] = [], 
            relations: list[Relation] = [],
            attributes: list[Attribute] = [],
            modifiers: list[Modifier] = [],
    ) -> None:
        self.entities = {}
        for entity in entities:
            self.entities[entity.name] = entity

        self.relations = {}
        for relation in relations:
            self.relations[relation.name] = relation

        self.attributes = {}
        for attribute in attributes:
            self.attributes[attribute.name] = attribute

        self.modifiers = {}
        for modifier in modifiers:
            self.modifiers[modifier.name] = modifier


    def interpret_relation(self, relation_name: str, values: list[any]) -> list[list[any]]:
        return []


    def interpret_entity(self, entity_name: str) -> list[any]:
        return Range(entity_name, [])
    

    def interpret_attribute(self, entity_name: str, attribute: str, values: list[any]) -> list[any]:
        return []
    