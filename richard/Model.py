from dataclasses import dataclass

from richard.ModelAdapter import ModelAdapter
from richard.entity.Instance import Instance
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


    def get_entity_range(self, entity: str) -> Range:
        if not entity in self.adapter.entities:
            raise Exception('No entity ' + entity + " in model")
        
        results = self.adapter.interpret_entity(entity)
        return self.hydrate_entities(results, entity)


    def find_relation_values(self, relation: str, field_values: list[list[Simple]], two_ways: bool = False):
        if not relation in self.adapter.relations:
            raise Exception('No relation ' + relation + " in model")
          
        if two_ways:
            results = self.adapter.interpret_relation(relation, field_values) + \
            self.adapter.interpret_relation(relation, reversed(field_values))
        else:
            results = self.adapter.interpret_relation(relation, field_values)

        return self.hydrate_relations(results, relation)

    
    def find_attribute_values(self, attribute: str, np: callable) -> Range:
        if not attribute in self.adapter.attributes:
            raise Exception('No attribute ' + attribute + " in model")
        
        results = []
        for instance in np():
            values = [None, instance.id]
            for f in self.adapter.interpret_attribute(instance.entity, attribute, values): 
                results.append(self.hydrate_attribute_value(f[0], attribute))

        return results


    def find_attribute_objects(self, attribute: str, np: callable) -> Range:
        if not attribute in self.adapter.attributes:
            raise Exception('No attribute ' + attribute + " in model")

        results = []
        for instance in np():
            values = [instance.id, None]
            for f in self.adapter.interpret_attribute(instance.entity, attribute, values):
                results.append(self.hydrate_attribute_object(f[1], instance.entity, attribute))

        return results
    

    def find_entity_with_highest_attribute_value(self, range: list, attribute: str) -> Range:
        """
        Returns a range with a single id from range, which is the id with the highest attribute value
        """
        max_instance = None
        max_result = None
        for instance in range:
            values = [None, instance.id]
            results = self.adapter.interpret_attribute(instance.entity, attribute, values)
            for r in results:
                if max_instance == None or max_result < r[0]:
                    max_instance = instance
                    max_result = r[0]
        return [max_instance]
    

    def find_entity_with_lowest_attribute_value(self, range: list, attribute: str) -> Range:
        """
        Returns a range with a single id from range, which is the id with the highest attribute value
        """
        max_instance = None
        max_result = None
        for instance in range:
            values = [None, instance.id]
            results = self.adapter.interpret_attribute(instance.entity, attribute, values)
            for r in results:
                if max_instance == None or max_result > r[0]:
                    max_instance = instance
                    max_result = r[0]
        return [max_instance]


    def filter_entities_by_modifier(self, range: Range, modifier: str) -> Range:
        """
        Returns the ids in range that match modifier
        """
        if not modifier in self.adapter.modifiers:
            raise Exception('No modifier ' + modifier + " in model")

        results = []
        for instance in range:
            for f in self.adapter.interpret_modifier(instance.entity, modifier, instance.id):
                results.append(Instance(instance.entity, f))

        return results


    def hydrate_entities(self, values: list[list[Simple]], entity: str) -> list[list[Instance]]:
        return [Instance(entity, element) for element in values]
            

    def hydrate_relations(self, values: list[list[Simple]], relation: str) -> list[list[Instance]]:
        hydrated = []
        relation = self.adapter.relations[relation]

        for row in values:
            h_row = []
            for i, element in enumerate(row):
                entity = relation.fields[i]
                h_row.append(Instance(entity, element))
            hydrated.append(h_row)

        return hydrated
    

    def hydrate_attribute_object(self, value: Simple, entity: str, attribute: str) -> Simple:
        # entity = self.adapter.entities[entity]
        attribute = self.adapter.attributes[attribute]
        if attribute.entity:
            return Instance(attribute.entity, value)
        else:
            return value


    def hydrate_attribute_value(self, value: Simple, attribute: str) -> Simple:
        attribute = self.adapter.attributes[attribute]
        if attribute.entity:
            return Instance(attribute.entity, value)
        else:
            return value
        
