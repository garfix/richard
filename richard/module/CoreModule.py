

from richard.constants import IGNORED, INFINITE, LARGE, ONE, UNKNOWN
from richard.entity.Relation import Relation
from richard.entity.Variable import Variable
from richard.interface.SomeModule import SomeModule
from richard.interface.SomeSolver import SomeSolver
from richard.type.OrderedSet import OrderedSet


class CoreModule(SomeModule):

    def __init__(self) -> None:
        self.relations = {
            "==": Relation(self.equals),
            ">": Relation(self.greater_than),
            "<": Relation(self.less_than),
            "aggregate": Relation(self.aggregation),
            "sum": Relation(self.sum),
            "avg": Relation(self.avg),
            "percentage": Relation(self.percentage),
            "count": Relation(self.count),
            "not": Relation(self.not_function),
            "=": Relation(self.assign),
            "det_equals": Relation(self.determiner_equals),
            "det_greater_than": Relation(self.determiner_greater_than),
            "all": Relation(self.determiner_all),
            "none": Relation(self.determiner_none),
        }
    

    # ('==', E1, E2)
    def equals(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:

        e1 = values[0]
        e2 = values[1]

        if isinstance(e1, Variable):
            if isinstance(e2, Variable):
                raise Exception("== is called with two variables")
            else:
                return [[e2, e2]]
        else:
            if isinstance(e2, Variable):
                return [[e1, e1]]

        if e1 == e2:
            return [[e1, e2]]
        return []


    # ('>', E1, E2)
    # E1 and E2 must be bound
    def greater_than(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:

        if values[0] > values[1]:
            return [values]
        return []


    # ('<', E1, E2)
    # E1 and E2 must be bound
    def less_than(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:

        if values[0] < values[1]:
            return [values]
        return []


    # ('aggregate', nbar, superlative, E1)
    # ('aggregation', E1, E2, [('size_of', E1, E2)], 'min')
    def aggregation(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:
        nbar, superlative, result_var = values
        predicate1, entity_var, attribute_var, argument_atoms, aggregation = superlative

        entities = solver.solve_for(nbar, binding, entity_var.name)

        attribute_values = []

        for entity in entities:
            attribute_binding = binding.copy()
            attribute_binding[entity_var.name] = entity
            values = solver.solve_for(argument_atoms, attribute_binding, attribute_var.name)
            if len(values) > 1:
                raise Exception((str(argument_atoms) + " returned " + str(len(values)) + " values; should be 1"))
            if len(values) == 0:
                raise Exception((str(argument_atoms) + " returned no values; should be 1"))
            attribute_values.append(values[0])

        best_value = None
        best_entity = None

        for entity, attribute_value in zip(entities, attribute_values):
            found = False
            if aggregation == "max":
                if best_value == None or attribute_value > best_value:
                    found = True
            elif aggregation == "min":
                if best_value == None or attribute_value < best_value:
                    found = True
            else: 
                raise Exception("Unknown aggregation: " + aggregation)
            if found:
                best_value = attribute_value
                best_entity = entity

        return [
            [None, None, best_entity]
        ]

    # ('count', E1, [body-atoms])
    # returns the number of results of body-atoms in E1
    def count(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:

        count_var, body = values

        results = solver.solve(body, binding)
        count = len(results)

        return [
            [count, None]
        ]
    

    # ('sum', E1, E2, [body-atoms])
    # returns the sum of results of the values of E2 in body-atoms in E1
    def sum(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:

        sum_var, element_var, body = values

        results = solver.solve(body, binding)
        s = 0
        for result in results:
            s += result[element_var.name]

        return [
            [s, None, None]
        ]


    # ('avg', E1, E2, [body-atoms])
    # returns the average of results of the values of E2 in body-atoms in E1
    def avg(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:

        sum_var, element_var, body = values

        results = solver.solve(body, binding)

        if len(results) == 0:
            return []

        s = 0
        n = 0
        for result in results:
            s += result[element_var.name]
            n += 1

        average = s / n

        return [
            [average, None, None]
        ]


    # ('percentage', E1, [nominator-atoms], [denominator-atoms])
    # returns the percentage of nominator-atoms in denominator-atoms
    def percentage(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:

        pecentage_var, nominator, denominator = values

        nominator_results = solver.solve(nominator, binding)
        denominator_results = solver.solve(denominator, binding)

        if len(denominator_results) == 0:
            return []

        percentage = (len(nominator_results) / len(denominator_results)) * 100.0

        return [
            [percentage, None, None]
        ]


    # ('not', [body-atoms])
    # if body-atoms returns values, not returns an empty list
    # otherwise, it returns a list with a single value: True
    def not_function(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:

        body = values[0]

        results = solver.solve(body, binding)
        count = len(results)

        if count > 0:
            return []
        else:
            return [
                [True]
            ]


    # ('=', E1, 5)
    def assign(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:

        return [[
            values[1], values[1]
        ]]


    # ('det_equals', [body-atoms], E2)
    def determiner_equals(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:

        body, number = values

        results = solver.solve(body, binding)
        count = len(results)

        if count == number:
            return results
        else:
            return []


    # ('det_greater_than', [body-atoms], E2)
    def determiner_greater_than(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:

        body, number = values

        results = solver.solve(body, binding)
        count = len(results)

        if count > number:
            return results
        else:
            return []


    # ('all', E1, [range-atoms], [body-atoms])
    def determiner_all(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:

        # find_var, quant, body = values
        # predicate1, quant_var, det, nbar = quant

        quant_var, range, body = values

        entities = OrderedSet([binding[quant_var.name] for binding in solver.solve(range, binding)])

        # print(entities)

        range_count = len(entities)
        results = OrderedSet()
        for entity in entities:
            b = binding | {
                quant_var.name: entity
            }
            bindings = solver.solve(body, b)
            # print(body, b, bindings)
            if len(bindings) > 0:
                results.add(entity)

        result_count = len(results)

        success = result_count == range_count   

        # print(body, success, result_count, find, binding)

        if success:
            return [[result, None, None] for result in results]
        else:        
            return []
        

    # ('none', [body-atoms])
    def determiner_none(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:

        body = values[0]

        results = solver.solve(body, binding)
        count = len(results)

        if count == 0:
            return [
                [True, None, None]
            ]
        else:
            return []        
        