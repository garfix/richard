

from richard.interface.SomeModule import SomeModule
from richard.interface.SomeSolver import SomeSolver


class CoreModule(SomeModule):

    def get_relations(self):
        return [
            "check", 
            "==",
        ]

    def interpret_relation(self, relation_name: str, db_values: list, in_types: list[str], solver: SomeSolver, binding: dict) -> list[list]:
        if relation_name == "check":
            out_types = [None, None]
            db_values = self.check(db_values, solver, binding)
        elif relation_name == "==":
            out_types = [None, None]
            db_values = self.equals(db_values, solver, binding)
        else:
            db_values = []

        return db_values, out_types


    def check(self, values: list, solver: SomeSolver, binding: dict) -> list[list]:
        quant, body = values
        predicate1, var, det, nbar = quant
        predicate2, result_var, range_var, check = det

        print('check')

        # ('determiner', Result, Range, [('==', Result, Range)])

        entities = set([binding[var.name] for binding in solver.solve(nbar, binding)])
        print(nbar)
        # print(binding)
        print(set(entities))
        range = len(entities)
        result = 0
        for entity in set(entities):
            b = binding | {
                var.name: entity
            }
            bindings = solver.solve(body, b)
            # print(body, b, bindings)
            if len(bindings) > 0:
                result += 1
        
        binding = {
            range_var.name: range,
            result_var.name: result
        }
        # print(binding, check, entities)
        ok_bindings = solver.solve(check, binding)
        # print(ok_bindings)
        if len(ok_bindings) > 0:
            return [[entity] for entity in entities]
        else:        
            return []


    def equals(self, values: list, solver: SomeSolver, binding: dict):
        # print('==', values)
        if values[0] == values[1]:
            return [values]
        return []