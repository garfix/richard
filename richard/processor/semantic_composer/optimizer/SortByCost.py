import math
from richard.Model import Model
from richard.constants import IGNORED
from richard.entity.Variable import Variable


class SortByCost:

    def sort(self, composition: list[tuple], model: Model):
        if len(composition) == 0:
            return []
                
        result = self.sort_rest([], composition, model)

        return result
    

    def sort_rest(self, done: list[tuple], todo: list[tuple], model: Model) -> list[tuple]:

        if len(todo) == 0:
            return done

        bound_variables = set()
        for atom in done:
            for argument in atom[1:]:
                if isinstance(argument, Variable):
                    bound_variables.add(argument.name)
        
        results = []
        for atom in todo:
            cost = self.calculate_cost(atom, bound_variables, model)
            results.append({'atom': atom, 'cost': cost})

        results.sort(key=lambda result: result['cost'])

        sorted = [result['atom'] for result in results]

        return self.sort_rest(done + sorted[0:1], sorted[1:], model)

    
    def calculate_cost(self, atom: tuple, bound_variables: set, model: Model):
        """
        Based on "Efficient processing of interactive relational database queries in logic" - David H.D. Warren (1981)
        """
        predicate = atom[0]
        relations = model.find_relations(predicate)
        if len(relations) == 0:
            return 0

        costs = []
        for relation in relations:
            unbound_argument_size_product = 1
            arguments = atom[1:]

            if len(arguments) != len(relation.argument_sizes):
                raise Exception("Number of argument sizes doesn't match that of relation: " + predicate)
            
            if relation.relation_size == IGNORED:
                cost = 100000000000
            else:

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

        return sum(costs)
    
    