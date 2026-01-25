from collections import defaultdict
from richard.core.atoms import bind_variables, convert_tuple_results_to_bindings, get_atom_variables
from richard.core.constants import DISJUNCTION
from richard.entity.BindingResult import BindingResult
from richard.entity.ResultIterator import ResultIterator
from richard.interface.SomeModel import SomeModel
from richard.interface.SomeSolver import SomeSolver
from richard.entity.ExecutionContext import ExecutionContext
from richard.processor.semantic_composer.SemanticSentence import SemanticSentence


class Solver(SomeSolver):

    model: SomeModel
    log_stats: bool
    stats: dict
    sentence: SemanticSentence

    def __init__(self, model: SomeModel, sentence: SemanticSentence=None, log_stats: bool=False) -> None:
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
        parameters = atom[1:]

        # predicate stats
        if self.log_stats:
            if not predicate in self.stats:
                self.stats[predicate] = 0
            self.stats[predicate] += 1

        if predicate == DISJUNCTION:
            return self.solve_disjunction(atom[1], binding)

        out_values = self.find_relation_values(predicate, parameters, binding)

        if isinstance(out_values, ResultIterator):
            return out_values

        if isinstance(out_values, BindingResult):
            completed_values = [binding | out_value for out_value in out_values]
            return list(completed_values)

        if isinstance(out_values, list):
            if len(out_values) > 0:
                if not isinstance(out_values[0], list) and not isinstance(out_values[0], tuple):
                    raise Exception("The results of '" + predicate + "' should be lists or tuples")
                if len(out_values[0]) != len(parameters):
                    raise Exception("The number of arguments in the results of '" + predicate + "' is " + str(len(out_values[0])) + " and should be " + str(len(parameters)))

            results = convert_tuple_results_to_bindings(predicate, out_values, binding, parameters)
            return results

        raise Exception("Predicate '" + predicate + "' should return a list")


    def solve_disjunction(self, disjuncts: list[list[tuple]], binding: dict):
        for disjunct in disjuncts:
            results = self.solve(disjunct, binding)
            if len(results) > 0:
                return results
        return []


    def find_relation_values(self, predicate: str, parameters: list, binding: dict) -> list[list]:

        relations = self.model.find_relations(predicate)
        if len(relations) == 0:
            raise Exception("No relation called '" + predicate + "' available in the model")

        arguments = bind_variables(parameters, binding)
        rows = []
        stringed_values = {}

        for relation in relations:
            context = ExecutionContext(relation, parameters, binding, self, self.sentence, self.model)

            # call the relation's query function
            out_values = relation.query_function(arguments, context)

            if isinstance(out_values, BindingResult):
                return out_values

            if isinstance(out_values, ResultIterator):
                if len(relations) > 1:
                    raise Exception("A relation that returns a ResultIterator can't be used in combination with another relation by the same name: " + relation.predicate)
                return out_values

            if not isinstance(out_values, list):
                raise Exception("The results of '" + predicate + "' should be a list")

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

        relations = self.model.find_relations(predicate)
        if len(relations) == 0:
            raise Exception("No relation called '" + predicate + "' available in the model")

        if len(get_atom_variables(arguments)) > 0:
            raise Exception(f"'{predicate}' attempts to persist a variable: {arguments}")

        # print(atom)

        for relation in relations:
            if relation.write_function is not None:
                context = ExecutionContext(relation, arguments, {}, self, self.sentence, self.model)
                relation.write_function(arguments, context)

