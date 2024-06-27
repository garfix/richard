

from richard.interface.SomeModule import SomeModule
from richard.interface.SomeSolver import SomeSolver

EXISTS = 'exists'

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

        entities = set([binding[var.name] for binding in solver.solve(nbar, binding)])
        range = len(entities)
        result = 0
        for entity in set(entities):
            b = binding | {
                var.name: entity
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

        if success:
            return [[entity] for entity in entities]
        else:        
            return []


    def equals(self, values: list, solver: SomeSolver, binding: dict):
        if values[0] == values[1]:
            return [values]
        return []