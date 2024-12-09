from collections import defaultdict
from richard.core.Model import Model
from richard.entity.ResultIterator import ResultIterator
from richard.entity.Variable import Variable
from richard.interface.SomeSolver import SomeSolver
from richard.type.ExecutionContext import ExecutionContext


class Solver(SomeSolver):

    model: Model
    log_stats: bool
    stats: dict

    def __init__(self, model: Model, log_stats: bool=False) -> None:
        self.model = model
        self.log_stats = log_stats
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

        # predicate stats
        if self.log_stats:
            if not predicate in self.stats:
                self.stats[predicate] = 0
            self.stats[predicate] += 1

        values = self.find_relation_values(predicate, arguments, binding)

        if isinstance(values, ResultIterator):
            return values

        if not isinstance(values, list):
            raise Exception("Predicate '" + predicate + "' should return a list")

        if len(values) > 0:
            if not isinstance(values[0], list):
                raise Exception("The results of '" + predicate + "' should be lists")
            if len(values[0]) != len(arguments):
                raise Exception("The number of arguments in the results of '" + predicate + "' is " + str(len(values[0])) + " and should be " + str(len(arguments)))

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
                else:
                    if v[i] is not None and arg != v[i]:
                        conflict = True

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
            context = ExecutionContext(relation, arguments, binding, self)

            # call the relation's query function
            out_values = relation.query_function(db_values, context)

            if isinstance(out_values, ResultIterator):
                if len(relations) > 1:
                    raise Exception("A relation that returns a ResultIterator can't be used in combination with another relation by the same name: " + relation.predicate)
                return out_values

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
                context = ExecutionContext(relation, arguments, {}, self)
                relation.write_function(arguments, context)

