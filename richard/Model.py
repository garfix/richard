from dataclasses import dataclass

from richard.ModelAdapter import ModelAdapter
from richard.entity.Instance import Instance
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


    def get_instances(self, entity_name: str) -> set[Instance]:
        if not entity_name in self.adapter.entities:
            raise Exception('No entity ' + entity_name + " in model")
        
        results = self.adapter.interpret_entity(entity_name)
        return self.hydrate_entities(results, entity_name)


    def find_relation_values(self, relation_name: str, field_values: set[Simple], two_ways: bool = False) -> list[list[Simple]]:
        if not relation_name in self.adapter.relations:
            raise Exception('No relation ' + relation_name + " in model")
          
        if two_ways:
            results = self.adapter.interpret_relation(relation_name, field_values) + \
                self.adapter.interpret_relation(relation_name, reversed(field_values))
        else:
            results = self.adapter.interpret_relation(relation_name, field_values)

        return self.hydrate_relations(results, relation_name)

    
    def find_attribute_values(self, attribute_name: str, range: callable) -> set[Simple]:
        if not attribute_name in self.adapter.attributes:
            raise Exception('No attribute ' + attribute_name + " in model")
        attribute = self.adapter.attributes[attribute_name]
        
        results = set()
        for instance in range():
            values = [None, instance.id]
            for f in self.adapter.interpret_attribute(instance.entity, attribute_name, values): 
                results.add(self.hydrate_attribute_value(f[0], attribute.entities[0], attribute_name))

        return results


    def find_attribute_objects(self, attribute_name: str, range: callable) -> set[Simple]:
        if not attribute_name in self.adapter.attributes:
            raise Exception('No attribute ' + attribute_name + " in model")
        attribute = self.adapter.attributes[attribute_name]

        results = set()
        for instance in range():
            values = [instance.id, None]
            for f in self.adapter.interpret_attribute(instance.entity, attribute_name, values):
                results.add(self.hydrate_attribute_object(f[1], attribute.entities[1], attribute_name))

        return results
    

    def find_entity_with_highest_attribute_value(self, range: callable, attribute_name: str) -> set[Instance]:
        """
        Returns a set with a single id from range, which is the id with the highest attribute value
        """
        max_instance = None
        max_result = None
        for instance in range():
            values = [None, instance.id]
            results = self.adapter.interpret_attribute(instance.entity, attribute_name, values)
            for r in results:
                if max_instance == None or max_result < r[0]:
                    max_instance = instance
                    max_result = r[0]
        return set([max_instance])
    

    def find_entity_with_lowest_attribute_value(self, range: callable, attribute_name: str) -> set[Instance]:
        """
        Returns a range with a single id from range, which is the id with the highest attribute value
        """
        max_instance = None
        max_result = None
        for instance in range():
            values = [None, instance.id]
            results = self.adapter.interpret_attribute(instance.entity, attribute_name, values)
            for r in results:
                if max_instance == None or max_result > r[0]:
                    max_instance = instance
                    max_result = r[0]
        return set([max_instance])


    def filter_by_modifier(self, range: callable, modifier_name: str) -> set[Instance]:
        """
        Returns the instances in range that match modifier
        """
        if not modifier_name in self.adapter.modifiers:
            raise Exception('No modifier ' + modifier_name + " in model")

        results = set()
        for instance in range():
            for f in self.adapter.interpret_modifier(instance.entity, modifier_name, instance.id):
                results.add(Instance(instance.entity, f))

        return results


    def hydrate_entities(self, ids: set[Simple], entity_name: str) -> set[Instance]:
        return set([Instance(entity_name, id) for id in ids])
            

    def hydrate_relations(self, values: set[list[Simple]], relation_name: str) -> list[list[Instance]]:
        hydrated = []
        relation = self.adapter.relations[relation_name]

        for row in values:
            h_row = []
            for i, element in enumerate(row):
                entity = relation.fields[i]
                h_row.append(Instance(entity, element))
            hydrated.append(h_row)

        return hydrated
    

    def hydrate_attribute_object(self, value: Simple, entity_name: str, attribute_name: str) -> Simple:
        # entity = self.adapter.entities[entity]
        attribute = self.adapter.attributes[attribute_name]
        if attribute.entities[1]:
            return Instance(attribute.entities[1], value)
        else:
            return value


    def hydrate_attribute_value(self, value: Simple, entity_name: str, attribute_name: str) -> Simple:
        attribute = self.adapter.attributes[attribute_name]
        if attribute.entities[0]:
            return Instance(attribute.entities[0], value)
        else:
            return value
        
