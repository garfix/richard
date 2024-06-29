

from richard.constants import EXISTS
from richard.interface.SomeModule import SomeModule
from richard.interface.SomeSolver import SomeSolver


class CoreModule(SomeModule):

    def get_relations(self):
        return [
            "check", 
            "==",
        ]
    

    def interpret_relation(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:
        if relation == "check":
            out_values = self.check(values, solver, binding)
        elif relation == "==":
            out_values = self.equals(values, solver, binding)
        else:
            out_values = []

        return out_values


    def check(self, values: list, solver: SomeSolver, binding: dict) -> list[list]:
        check_var, quant, body = values
        predicate1, quant_var, det, nbar = quant

        entities = set([binding[quant_var.name] for binding in solver.solve(nbar, binding)])

        # print('check', entities)

        range = len(entities)
        result = 0
        for entity in set(entities):
            b = binding | {
                quant_var.name: entity
            }
            bindings = solver.solve(body, b)
            if len(bindings) > 0:
                result += 1        

        if det == EXISTS:
            success = result > 0   
        else:
            predicate2, result_var, range_var, check = det

            binding = {
                range_var.name: range,
                result_var.name: result
            }
            ok_bindings = solver.solve(check, binding)
            success = len(ok_bindings) > 0

        # print('end check', success, [[entity, None, None] for entity in entities])

        if success:
            return [[entity, None, None] for entity in entities]
        else:        
            return []


    def equals(self, values: list, solver: SomeSolver, binding: dict):
        if values[0] == values[1]:
            return [values]
        return []
    