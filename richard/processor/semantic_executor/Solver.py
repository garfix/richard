from richard.Model import Model
from richard.entity.Variable import Variable


class Solver:

    model: Model

    def __init__(self, model: Model) -> None:
        self.model = model


    def solve(self, tuples: list[tuple], binding: dict = {}) -> list[dict]:
        if len(tuples) == 0:
            return [binding]
        
        result = []
        bindings = self.solve_single(tuples[0], binding)
        for b in bindings:
            result += self.solve(tuples[1:], b)
        return result


    def solve_single(self, tuple: tuple, binding: dict = {}):
        relation = tuple[0]
        arguments = tuple[1:]

        prepared = []
        for arg in arguments:
            if isinstance(arg, Variable):
                if arg.name in binding:
                    prepared.append(binding[arg.name])   
                else: 
                    prepared.append(None)
            else:
                prepared.append(arg)

        print(prepared)

        values = self.model.find_relation_values(relation, prepared)

        print(values)

        results = []
        for v in values:
            result = binding.copy()
            for i, arg in enumerate(arguments):
                if isinstance(arg, Variable):
                    result[arg.name] = v[i]
            results.append(result)
        return results
    