from collections import defaultdict
from richard.core.functions.terms import bind_variables, get_variables
from richard.core.functions.results import tuple_results_to_bindings
from richard.core.constants import DISJUNCTION
from richard.entity.BindingResult import BindingResult
from richard.interface.SomeModel import SomeModel
from richard.interface.SomeSolver import SomeSolver
from richard.entity.ExecutionContext import ExecutionContext
from richard.processor.semantic_composer.SemanticSentence import SemanticSentence


class Solver(SomeSolver):

    model: SomeModel
    sentence: SemanticSentence

    def __init__(self, model: SomeModel, sentence: SemanticSentence=None) -> None:
        self.model = model
        self.sentence = sentence


    def solve(self, atoms: list[tuple]) -> list[dict]:
        if not isinstance(atoms, list):
            raise Exception("Solver can only solve lists of atoms, this is not a list: " + str(atoms))

        return self.solve_rest(atoms, {})


    def solve_rest(self, atoms: list[tuple], binding: dict = {}) -> list[dict]:
        if len(atoms) == 0:
            return [binding]
        else:
            result = []
            bindings = self.solve_single(atoms[0], binding)
            for b in bindings:
                result.extend(self.solve_rest(atoms[1:], b))
            return result


    def solve_single(self, atom: tuple, binding: dict):
        predicate = atom[0]
        unbound_arguments = atom[1:]

        if predicate == DISJUNCTION:
            return self.solve_disjunction(atom[1], binding)

        arguments = bind_variables(unbound_arguments, binding)
        out_bindings = self.find_relation_values(predicate, arguments, binding)

        return out_bindings


    def solve_disjunction(self, disjuncts: list[list[tuple]], binding: dict):
        for disjunct in disjuncts:
            results = self.solve(disjunct)
            if len(results) > 0:
                return results
        return []


    def find_relation_values(self, predicate: str, arguments: list, binding: dict) -> list[list]:

        relations = self.model.find_relations(predicate)
        if len(relations) == 0:
            raise Exception("No relation called '" + predicate + "' available in the model")

        deduplicated_bindings = {}

        for relation in relations:
            context = ExecutionContext(relation, self, self.sentence, self.model)

            # call the relation's query function
            out_values = relation.query_function(arguments, context)

            if isinstance(out_values, BindingResult):

                # note: only one predicate can have a BindingResult, at this time
                # also: no validity checks are done, nor deduplication
                completed_values = [binding | out_value for out_value in out_values]
                return list(completed_values)

            elif isinstance(out_values, list):

                if len(out_values) > 0:
                    if not isinstance(out_values[0], list) and not isinstance(out_values[0], tuple):
                        raise Exception("The results of '" + predicate + "' should be lists or tuples")
                    if len(out_values[0]) != len(arguments):
                        raise Exception("The number of arguments in the results of '" + predicate + "' is " + str(len(out_values[0])) + " and should be " + str(len(unbound_arguments)))

                out_bindings = tuple_results_to_bindings(predicate, arguments, out_values, binding)

                # deduplicate results
                for out_binding in out_bindings:
                    deduplicated_bindings[str(out_binding)] = out_binding

            else:
                raise Exception("The result of '" + predicate + "' should be a list")

        return deduplicated_bindings.values()


    def write_atom(self, atom: tuple):
        predicate = atom[0]
        arguments = atom[1:]

        relations = self.model.find_relations(predicate)
        if len(relations) == 0:
            raise Exception("No relation called '" + predicate + "' available in the model")

        if len(get_variables(arguments)) > 0:
            raise Exception(f"'{predicate}' attempts to persist a variable: {arguments}")

        # print(atom)

        for relation in relations:
            if relation.write_function is not None:
                context = ExecutionContext(relation, self, self.sentence, self.model)
                relation.write_function(arguments, context)


    def write_atoms(self, atoms: list[tuple]):
        for atom in atoms:
            self.write_atom(atom)
