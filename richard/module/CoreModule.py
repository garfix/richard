

from richard.interface.SomeModule import SomeModule
from richard.interface.SomeSolver import SomeSolver


class CoreModule(SomeModule):
    def interpret_relation(self, relation_name: str, values: list, solver: SomeSolver) -> list[list]:
        if relation_name == "check":
            return self.check(values, solver)
        else:
            return []


    def check(self, values: list, solver: SomeSolver):
        quant, body = values
        predicate1, var, det, nbar = quant
        predicate2, result_var, range_var, check = det

        print('check')

        # ('determiner', Result, Range, [('==', Result, Range)])

        entities = [binding[var.name] for binding in solver.solve(nbar)]
        # print(entities)
        range = len(entities)
        result = 0
        for entity in set(entities):
            binding = {
                var.name: entity
            }
            print(binding)
            print(body)
            bindings = solver.solve(body, binding)
            if len(bindings) > 0:
                result += 1
        
        binding = {
            range_var: range,
            result_var: result
        }
        ok_bindings = solver.solve([check], binding)
        if len(ok_bindings) > 0:
            return entities
        else:        
            return []
