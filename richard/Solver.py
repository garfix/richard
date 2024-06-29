from richard.Model import Model
from richard.entity.Variable import Variable
from richard.interface.SomeSolver import SomeSolver

# d = 0

class Solver(SomeSolver):

    model: Model

    def __init__(self, model: Model) -> None:
        self.model = model


    def solve(self, tuples: list[tuple], binding: dict) -> list[dict]:
        # global d
        # print("   " * d, "s", tuples, binding)
        if len(tuples) == 0:
            result = [binding]
        else:
            # d += 1

            result = []
            bindings = self.solve_single(tuples[0], binding)
            if len(tuples) == 1:
                result = bindings
                # print("bindings", bindings)
            else:
                for b in bindings:
                    result.extend(self.solve(tuples[1:], b))
                    # print("   " * d, tuples[1:], b, result)

            # d -= 1  

        # print("e", tuples, binding, result)
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
        # print("values", values, len(arguments))

        results = []
        for v in values:
            # extend the incoming binding
            result = binding.copy()
            # check needed for a variable that occurs twice
            conflict = False

            # go through all arguments
            for v1, arg in zip(v, arguments):
                # print('arg', arg)
                # variable?
                if isinstance(arg, Variable):
                    # check for conflict with previous same variable
                    if arg.name in result and result[arg.name] != v1:
                        conflict = True
                    # extend the binding
                    result[arg.name] = v1

            if conflict:
                continue

            results.append(result)
            
        return results
    