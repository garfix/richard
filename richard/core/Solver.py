from collections import defaultdict
from richard.core.Model import Model
from richard.core.atoms import bind_variables
from richard.core.constants import DISJUNCTION
from richard.entity.BindingResult import BindingResult
from richard.entity.Relation import Relation
from richard.entity.ResultIterator import ResultIterator
from richard.entity.Variable import Variable
from richard.interface.SomeSolver import SomeSolver
from richard.entity.ExecutionContext import ExecutionContext
from richard.processor.semantic_composer.SemanticSentence import SemanticSentence


class Solver(SomeSolver):

    model: Model
    log_stats: bool
    stats: dict
    sentence: SemanticSentence

    def __init__(self, model: Model, sentence: SemanticSentence=None, log_stats: bool=False) -> None:
        self.model = model
        self.log_stats = log_stats
        self.stats = defaultdict(lambda: 0)
        self.sentence = sentence


    def solve(self, atoms: list[tuple], binding: dict = {}) -> list[dict]:

        if not isinstance(atoms, list):
            raise Exception("Solver can only solve lists of atoms, this is not a list: " + str(atoms))

        if len(atoms) == 1:
            return self.solve_single(atoms[0], binding)
        if len(atoms) == 0:
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

        if predicate == DISJUNCTION:
            return self.solve_disjunction(atom[1], binding)

        values = self.find_relation_values(predicate, arguments, binding)

        if isinstance(values, ResultIterator):
            return values

        if isinstance(values, BindingResult):
            completed_values = [binding | out_value for out_value in values]
            return list(completed_values)

        if not isinstance(values, list):
            raise Exception("Predicate '" + predicate + "' should return a list")

        if len(values) > 0:
            if not isinstance(values[0], list) and not isinstance(values[0], tuple):
                raise Exception("The results of '" + predicate + "' should be lists or tuples")
            if len(values[0]) != len(arguments):
                raise Exception("The number of arguments in the results of '" + predicate + "' is " + str(len(values[0])) + " and should be " + str(len(arguments)))

        results = self.create_solve_single_results(values, binding, arguments)
        return results


    def create_solve_single_results(self, values: list, binding: dict, arguments: list):
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


    def solve_disjunction(self, disjuncts: list[list[tuple]], binding: dict):
        for disjunct in disjuncts:
            results = self.solve(disjunct, binding)
            if len(results) > 0:
                return results
        return []

    def find_relations(self, relation: str) -> list[Relation]:
        result = []
        for module in self.model.modules:
            relations = module.get_relations()
            if relation in relations:
                result.append(relations[relation])
        return result


    def find_relation_values(self, predicate: str, arguments: list, binding: dict) -> list[list]:

        relations = self.find_relations(predicate)
        if len(relations) == 0:
            raise Exception("No relation called '" + predicate + "' available in the model")

        db_values = bind_variables(arguments, binding)

        rows = []
        stringed_values = {}

        for relation in relations:
            context = ExecutionContext(relation, arguments, binding, self, self.sentence)

            # call the relation's query function
            out_values = relation.query_function(db_values, context)

            if isinstance(out_values, BindingResult):
                return out_values

            if isinstance(out_values, ResultIterator):
                if len(relations) > 1:
                    raise Exception("A relation that returns a ResultIterator can't be used in combination with another relation by the same name: " + relation.predicate)
                return out_values

            # deduplicate results
            for out_value in out_values:
                stringed_value = str(out_value)
                if stringed_value not in stringed_values:
                    stringed_values[stringed_value] = out_value
                    rows.append(out_value)

        return rows


    def write_atom(self, atom: tuple):
        predicate = atom[0]
        arguments = atom[1:]

        relations = self.find_relations(predicate)
        if len(relations) == 0:
            raise Exception("No relation called '" + predicate + "' available in the model")

        for relation in relations:
            if relation.write_function is not None:
                context = ExecutionContext(relation, arguments, {}, self, self.sentence)
                relation.write_function(arguments, context)

