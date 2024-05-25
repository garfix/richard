from dataclasses import dataclass

from richard.ModelAdapter import ModelAdapter
from richard.entity.Range import Range
from richard.semantics.commands import dnp
from richard.type.Simple import Simple


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


    def get_entity_range(self, entity_name: str) -> Range:
        if not entity_name in self.adapter.entities:
            raise Exception('No entity ' + entity_name + " in model")
        
        return Range(entity_name, self.adapter.interpret_entity(entity_name))


    def relation_exists(self, relation_name: str, field_values: list[Simple]):
        if not relation_name in self.adapter.relations:
            raise Exception('No relation ' + relation_name + " in model")
          
        return self.adapter.interpret_relation(relation_name, field_values)
    

    def get_matching_attribute_range(self, attribute_name: str, dnp: dnp) -> Range:
        if not attribute_name in self.adapter.attributes:
            raise Exception('No attribute ' + attribute_name + " in model")

        range = dnp.nbar()
        results = []
        for id in range:
            values = [None, id]
            for f in self.adapter.interpret_attribute(range.entity, attribute_name, values): # todo untyped
                results.append(f[0])

        if dnp.determiner(len(results), len(range)):
            return results
        else:
            return Range(range.entity, [])
        

    def find_range_attribute_max(self, range: Range, attribute_name: str) -> Range:
        max_id = None
        max_result = None
        for id in range:
            values = [None, id]
            results = self.adapter.interpret_attribute(range.entity, attribute_name, values)
            for r in results:
                if max_id == None or max_result < r:
                    max_id = id
                    max_result = r
        return Range(range.entity, [max_id])
    

    def filter_by_modifier(self, range: Range, modifier_name: str) -> Range:
        if not modifier_name in self.adapter.modifiers:
            raise Exception('No modifier ' + modifier_name + " in model")
        
        results = []
        for id in range:
            for f in self.adapter.interpret_modifier(range.entity, modifier_name, id):
                results.append(f)

        print(results, range.entity, modifier_name)


        return Range(range.entity, results)
