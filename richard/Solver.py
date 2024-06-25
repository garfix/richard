from richard.Model import Model
from richard.entity.Variable import Variable
from richard.interface.SomeSolver import SomeSolver


class Solver(SomeSolver):

    model: Model

    def __init__(self, model: Model) -> None:
        self.model = model


    def solve(self, tuples: list[tuple], binding: dict) -> list[dict]:
        if len(tuples) == 0:
            return [binding]
        
        result = []
        bindings = self.solve_single(tuples[0], binding)
        for b in bindings:
            result += self.solve(tuples[1:], b)
        return result


    def solve_single(self, tuple: tuple, binding: dict):
        relation = tuple[0]
        arguments = tuple[1:]

        prepared = []
        for arg in arguments:
            # variable
            if isinstance(arg, Variable):
                # bound?
                if arg.name in binding:
                    # add variable value
                    prepared.append(binding[arg.name])   
                else: 
                    # add None
                    prepared.append(None)
            else:
                # just add value
                prepared.append(arg)

        values = self.model.find_relation_values(relation, prepared, self, binding)
        # print(values)

        results = []
        for v in values:
            # extend the incoming binding
            result = binding.copy()
            # check needed for a variable that occurs twice
            conflict = False

            # go through all arguments
            for i, arg in enumerate(arguments):
                # variable?
                if isinstance(arg, Variable):
                    # check for conflict with previous same variable
                    if arg.name in result and result[arg.name] != v[i]:
                        conflict = True
                    # extend the binding
                    result[arg.name] = v[i]

            if conflict:
                continue

            results.append(result)
            
        return results
    