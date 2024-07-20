

from richard.constants import EXISTS
from richard.interface.SomeModule import SomeModule
from richard.interface.SomeSolver import SomeSolver


class CoreModule(SomeModule):

    def get_relations(self):
        return [
            "find", 
            "==",
            "aggregate",
        ]
    

    def interpret_relation(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:
        if relation == "find":
            out_values = self.find(values, solver, binding)
        elif relation == "==":
            out_values = self.equals(values, solver, binding)
        elif relation == "aggregate":
            out_values = self.aggregation(values, solver, binding)
        else:
            out_values = []

        return out_values

    # ('find', E1, np, vp_nosub_obj)
    # ('quant', E1, det, nbar)
    def find(self, values: list, solver: SomeSolver, binding: dict) -> list[list]:
        find_var, quant, body = values
        predicate1, quant_var, det, nbar = quant

        entities = set([binding[quant_var.name] for binding in solver.solve(nbar, binding)])

        range = len(entities)
        results = []
        for entity in set(entities):
            b = binding | {
                quant_var.name: entity
            }
            bindings = solver.solve(body, b)
            if len(bindings) > 0:
                results.append(entity)

        result_count = len(results)

        if det == EXISTS:
            success = result_count > 0   
        else:
            predicate2, result_var, range_var, find = det

            binding = {
                range_var.name: range,
                result_var.name: result_count
            }
            ok_bindings = solver.solve(find, binding)
            success = len(ok_bindings) > 0

        if success:
            return [[result, None, None] for result in results]
        else:        
            return []


    # ('==', E1, E2)
    def equals(self, values: list, solver: SomeSolver, binding: dict) -> list[list]:

        if values[0] == values[1]:
            return [values]
        return []
    

    # ('aggregate', nbar, superlative, E1)
    # ('aggregation', E1, E2, [('size-of', E1, E2)], 'min')
    def aggregation(self, values: list, solver: SomeSolver, binding: dict) -> list[list]:
        nbar, superlative, result_var = values
        predicate1, entity_var, attribute_var, argument_atoms, aggregation = superlative

        entities = solver.solve_for(nbar, binding, entity_var.name)

        attribute_values = []

        for entity in entities:
            attribute_binding = binding.copy()
            attribute_binding[entity_var.name] = entity
            values = solver.solve_for(argument_atoms, attribute_binding, attribute_var.name)
            if len(values) > 1:
                raise Exception((str(argument_atoms) + " returned " + str(len(values)) + " values; should be 1"))
            if len(values) == 0:
                raise Exception((str(argument_atoms) + " returned no values; should be 1"))
            attribute_values.append(values[0])

        best_value = None
        best_entity = None

        for entity, attribute_value in zip(entities, attribute_values):
            found = False
            if aggregation == "max":
                if best_value == None or attribute_value > best_value:
                    found = True
            elif aggregation == "min":
                if best_value == None or attribute_value < best_value:
                    found = True
            else: 
                raise Exception("Unknown aggregation: " + aggregation)
            if found:
                best_value = attribute_value
                best_entity = entity

        return [
            [None, None, best_entity]
        ]
