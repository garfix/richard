from dataclasses import dataclass

from richard.ModelAdapter import ModelAdapter
from richard.entity.Range import Range
from richard.entity.Attribute import Attribute
from richard.entity.Modifier import Modifier
from richard.entity.Relation import Relation
from richard.entity.Entity import Entity
from richard.semantics.commands import dnp


class Model:
    """
    This class represents the generic part of the model. Do not extend it. In stead, extend the adapter.
    """

    adapter: ModelAdapter


    def __init__(
            self, 
            adapter: ModelAdapter
    ) -> None:
        self.adapter = adapter


    def get_range(self, entity_name: str) -> Range:
        if not entity_name in self.adapter.entities:
            raise Exception('No entity ' + entity_name + " in model")
        
        return self.adapter.interpret_entity(entity_name)


    def relation_exists(self, relation_name: str, field_values: list[any]):
        if not relation_name in self.adapter.relations:
            raise Exception('No relation ' + relation_name + " in model")
          
        return self.adapter.interpret_relation(relation_name, field_values)

    def search_attribute(self, attribute_name: str, dnp: dnp):
        if not attribute_name in self.adapter.attributes:
            raise Exception('No attribute ' + attribute_name + " in model")

        elements = dnp.nbar()
        results = []
        for e in elements:
            values = [None, e]
            for f in self.adapter.interpret_attribute(elements.entity, attribute_name, values): # todo untyped
                results.append(f[0])

        if dnp.determiner(len(results), len(elements)):
            return results
        else:
            return []
        