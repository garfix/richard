from collections import defaultdict
from richard.Model import Model
from richard.entity.Variable import Variable
from richard.interface.SomeSolver import SomeSolver


class Solver(SomeSolver):

    model: Model
    stats: dict

    def __init__(self, model: Model) -> None:
        self.model = model
        self.stats = defaultdict(lambda: 0)


    def solve_for(self, atoms: list[tuple], binding: dict, variable: str) -> list[dict]:
        return [binding[variable] for binding in self.solve(atoms, binding)]


    def solve(self, atoms: list[tuple], binding: dict) -> list[dict]:

        if not isinstance(atoms, list):
            raise Exception("Solver can only solve lists of atoms, this is not a list: " + str(atoms))

        if len(atoms) == 1:
            return self.solve_single(atoms[0], binding)
        elif len(atoms) == 0:
            return [binding]
        else:
            result = []
            bindings = self.solve_single(atoms[0], binding)
            for b in bindings:
                for r in self.solve(atoms[1:], b):
                    if not r in result:
                        result.append(r)
            return result
    

    def solve_single(self, tuple: tuple, binding: dict):
        relation = tuple[0]
        arguments = tuple[1:]

        # self.stats[relation] += 1

        prepared = []
        for arg in arguments:
            # variable
            if isinstance(arg, Variable):
                # bound?
                if arg.name in binding:
                    # add variable value
                    prepared.append(binding[arg.name])   
                else: 
                    # add variable itself
                    prepared.append(arg)
            else:
                # just add value
                prepared.append(arg)

        values = self.model.find_relation_values(relation, prepared, self, binding)

        results = []
        for v in values:
            # extend the incoming binding
            result = binding.copy()
            # check needed for a variable that occurs twice
            conflict = False

            # go through all arguments
            i = 0
            for arg in arguments:
                # variable?
                if isinstance(arg, Variable):
                    # if the variable was bound already, no need to assign it
                    # also no need to check for conflict, because the type may be different and that's ok
                    if arg.name not in binding:
                        # check for conflict with previous same variable
                        if arg.name in result and result[arg.name] != v[i]:
                            conflict = True
                        # extend the binding
                        result[arg.name] = v[i]
                i += 1

            if conflict:
                continue

            results.append(result)
            
        return results
    