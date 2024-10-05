from richard.core.Model import Model
from richard.core.atoms import get_atom_variables
from richard.core.constants import IGNORED, INFINITE
from richard.entity.Variable import Variable


class SortByCost:
    """
    Based on "Efficient processing of interactive relational database queries in logic" - David H.D. Warren (1981)
    """

    def sort(self, composition: list[tuple], model: Model, bound_variables: set[str] = set()):
        if len(composition) == 0:
            return []

        result = self.sort_rest([], composition, model, bound_variables)

        return result


    def sort_rest(self, done: list[tuple], todo: list[tuple], model: Model, bound_variables: set[str]) -> list[tuple]:

        if len(todo) == 0:
            return done

        results = []
        for atom in todo:
            cost = self.calculate_cost(atom, bound_variables, model)
            results.append({'atom': atom, 'cost': cost})

        results.sort(key=lambda result: result['cost'])
        sorted = [result['atom'] for result in results]

        sorted_first_atom = self.sort_arguments(sorted[0], model, bound_variables)
        bound_variables = bound_variables | set(get_atom_variables(sorted_first_atom))

        return self.sort_rest(done + [sorted_first_atom], sorted[1:], model, bound_variables)


    def sort_arguments(self, atom: tuple, model: Model, bound_variables: set[str]) -> tuple:
        atom_as_list = list(atom)
        replaced = False
        for i, arg in enumerate(atom):
            if isinstance(arg, list):
                atom_as_list[i] = self.sort(arg, model, bound_variables)
                replaced = True
        if replaced:
            return tuple(atom_as_list)
        else:
            return atom


    def calculate_cost(self, atom: tuple, bound_variables: set, model: Model):
        predicate = atom[0]
        relations = model.find_relations(predicate)
        if len(relations) == 0:
            return 0

        costs = []
        for relation in relations:
            unbound_argument_size_product = 1
            arguments = atom[1:]

            if relation.relation_size == IGNORED:
                cost = INFINITE
            else:

                if len(arguments) != len(relation.argument_sizes):
                    raise Exception("Number of argument sizes doesn't match that of relation: " + predicate)

                for argument, argument_size in zip(arguments, relation.argument_sizes):

                    if argument_size == IGNORED:
                        pass
                    elif isinstance(argument, Variable):
                        if argument.name in bound_variables:
                            unbound_argument_size_product *= argument_size
                    elif isinstance(argument, list):
                        pass
                    elif isinstance(argument, tuple):
                        pass
                    else:
                        unbound_argument_size_product *= argument_size

                cost = relation.relation_size / unbound_argument_size_product

            costs.append(cost)

        # if the predicate occurs in multiple relations, take the maximal cost
        # (not the sum of the costs, because we don't want to double the cost with 2 simular relations)
        return max(costs)

