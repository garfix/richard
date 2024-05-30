from dataclasses import dataclass

from richard.entity.Instance import Instance
from richard.entity.Range import Range
from richard.entity.Attribute import Attribute
from richard.entity.Modifier import Modifier
from richard.entity.Relation import Relation
from richard.entity.Entity import Entity
from richard.type.Simple import Simple


class ModelAdapter:
    """
    This class represents the domain-specific part of the model. Extend it to fit your needs.
    """

    modifiers: dict[str, Modifier]
    attributes: dict[str, Attribute]
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

        self.do_consistency_check()


    def do_consistency_check(self):
        for attribute in self.attributes.values():
            for entity in attribute.entities:
                if entity and entity not in self.entities:
                    raise Exception("Attribute entity '" + attribute.entity + "' was not defined in the adapter")
                
        for entity in self.entities.values():
            for attribute in entity.attributes:
                if not attribute in self.attributes:
                    raise Exception("Entity attribute '" + attribute + "' was not defined in the adapter")
                
        for entity in self.entities.values():
            for modifier in entity.modifiers:
                if not modifier in self.modifiers:
                    raise Exception("Entity modifier '" + modifier + "' was not defined in the adapter")
        


    def interpret_relation(self, relation: str, values: list[Simple]) -> list[list[Simple]]:
        return []


    def interpret_entity(self, entity: str) -> list[Simple]:
        return Range(entity, [])
    

    def interpret_attribute(self, entity: str, attribute: str, values: list[Simple]) -> list[Simple]:
        return []
    
    
    def interpret_modifier(self, entity: str, modifier: str, value: Simple) -> list[Simple]:
        return []
