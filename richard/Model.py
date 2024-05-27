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


    def filter_entities(self, dnp: dnp, vp: callable = None) -> list:
        """
        Result consists of all elements in dnp.nbar that satisfy vp
        If the number of results agrees with dnp.determiner, results are returned. If not, an empty list
        """

        elements = dnp.range()
        range_count = len(elements)

        result = []
        if vp:
            for element in elements:
                # print(element)
                for e2 in vp(element):
                    result.append(element)
        else:
            result = elements

        result = list(set(result))
        result_count = len(result)
        
        if dnp.determiner(result_count, range_count):
            # print(dnp.range(), result)
            return Range(elements.entity, result)
        else:
            # print(dnp.range(), result)
            return Range(elements.entity, [])


    def find_relation_values(self, relation_name: str, field_values: list[list[Simple]]):
        if not relation_name in self.adapter.relations:
            raise Exception('No relation ' + relation_name + " in model")
          
        v=self.adapter.interpret_relation(relation_name, field_values)
        # print('v', v)
        return v

    

    def find_attribute_values(self, attribute_name: str, dnp: dnp) -> Range:
        if not attribute_name in self.adapter.attributes:
            raise Exception('No attribute ' + attribute_name + " in model")

        range = dnp.range()
        results = []
        for id in range:
            values = [None, id]
            for f in self.adapter.interpret_attribute(range.entity, attribute_name, values): # todo untyped
                results.append(f[0])

        if dnp.determiner(len(results), len(range)):
            return Range(range.entity, results)
        else:
            return Range(range.entity, [])
        

    def find_attribute_objects(self, attribute_name: str, dnp: dnp) -> Range:
        if not attribute_name in self.adapter.attributes:
            raise Exception('No attribute ' + attribute_name + " in model")

        range = dnp.range()
        results = []
        for id in range:
            values = [id, None]
            for f in self.adapter.interpret_attribute(range.entity, attribute_name, values): # todo untyped
                results.append(f[1])

        if dnp.determiner(len(results), len(range)):
            return results
        else:
            return Range(range.entity, [])


    def find_entity_with_highest_attribute_value(self, range: Range, attribute_name: str) -> Range:
        """
        Returns a range with a single id from range, which is the id with the highest attribute value
        """
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
    

    def find_entity_with_lowest_attribute_value(self, range: Range, attribute_name: str) -> Range:
        """
        Returns a range with a single id from range, which is the id with the highest attribute value
        """
        max_id = None
        max_result = None
        for id in range:
            values = [None, id]
            results = self.adapter.interpret_attribute(range.entity, attribute_name, values)
            for r in results:
                if max_id == None or max_result > r:
                    max_id = id
                    max_result = r
        return Range(range.entity, [max_id])


    def filter_entities_by_modifier(self, range: Range, modifier_name: str) -> Range:
        """
        Returns the ids in range that match modifier
        """
        if not modifier_name in self.adapter.modifiers:
            raise Exception('No modifier ' + modifier_name + " in model")
        
        results = []
        for id in range:
            for f in self.adapter.interpret_modifier(range.entity, modifier_name, id):
                results.append(f)

        return Range(range.entity, results)


