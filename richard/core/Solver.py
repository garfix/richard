from collections import defaultdict
from richard.core.Model import Model
from richard.entity.Variable import Variable
from richard.interface.SomeSolver import SomeSolver
from richard.type.ExecutionContext import ExecutionContext


class Solver(SomeSolver):

    model: Model
    stats: dict

    def __init__(self, model: Model) -> None:
        self.model = model
        self.stats = defaultdict(lambda: 0)


    def solve(self, atoms: list[tuple], binding: dict = {}) -> list[dict]:

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


    def solve_single(self, atom: tuple, binding: dict):
        predicate = atom[0]
        arguments = atom[1:]

        # if not predicate in self.stats:
        #     self.stats[predicate] = 0
        # self.stats[predicate] += 1

        values = self.find_relation_values(predicate, arguments, binding)

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
                    # if the variable was bound already, no need to assign it
                    # also no need to check for conflict, because the type may be different and that's ok
                    if arg.name not in binding:
                        # check for conflict with previous same variable
                        if arg.name in result and result[arg.name] != v[i]:
                            conflict = True
                        # extend the binding
                        result[arg.name] = v[i]

            if conflict:
                continue

            results.append(result)

        return results


    def find_relation_values(self, predicate: str, arguments: list, binding: dict) -> list[list]:

        relations = self.model.find_relations(predicate)
        if len(relations) == 0:
            raise Exception("No relation called '" + predicate + "' available in the model")

        db_values = self.model_values_2_db_values(arguments, binding)

        rows = []
        for relation in relations:
            context = ExecutionContext(relation, predicate, arguments, binding, self)
            out_values = relation.query_function(db_values, context)
            rows.extend(out_values)

        return rows


    def model_values_2_db_values(self, model_values: list, binding: dict) -> list:
        prepared = []
        for arg in model_values:
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

        return prepared


    def write_atom(self, atom: tuple):
        predicate = atom[0]
        arguments = atom[1:]

        relations = self.model.find_relations(predicate)
        if len(relations) == 0:
            raise Exception("No relation called '" + predicate + "' available in the model")

        for relation in relations:
            if relation.write_function is not None:
                context = ExecutionContext(relation, predicate, arguments, {}, self)
                relation.write_function(arguments, context)

