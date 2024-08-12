

from richard.entity.Relation import Relation
from richard.entity.Variable import Variable
from richard.interface.SomeModule import SomeModule
from richard.interface.SomeSolver import SomeSolver
from richard.type.ExecutionContext import ExecutionContext
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
    def equals(self, values: list, context: ExecutionContext) -> list[list]:

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
    def greater_than(self, values: list, context: ExecutionContext) -> list[list]:

        if values[0] > values[1]:
            return [values]
        return []


    # ('<', E1, E2)
    # E1 and E2 must be bound
    def less_than(self, values: list, context: ExecutionContext) -> list[list]:

        if values[0] < values[1]:
            return [values]
        return []


    # ('aggregate', nbar, superlative, E1)
    # ('aggregation', E1, E2, [('size_of', E1, E2)], 'min')
    def aggregation(self, values: list, context: ExecutionContext) -> list[list]:
        nbar, superlative, result_var = values
        predicate1, entity_var, attribute_var, argument_atoms, aggregation = superlative

        entities = context.solver.solve_for(nbar, context.binding, entity_var.name)

        attribute_values = []

        for entity in entities:
            attribute_binding = context.binding.copy()
            attribute_binding[entity_var.name] = entity
            values = context.solver.solve_for(argument_atoms, attribute_binding, attribute_var.name)
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
    def count(self, values: list, context: ExecutionContext) -> list[list]:

        count_var, body = values

        results = context.solver.solve(body, context.binding)
        count = len(results)

        return [
            [count, None]
        ]
    

    # ('sum', E1, E2, [body-atoms])
    # returns the sum of results of the values of E2 in body-atoms in E1
    def sum(self, values: list, context: ExecutionContext) -> list[list]:

        sum_var, element_var, body = values

        results = context.solver.solve(body, context.binding)
        s = 0
        for result in results:
            s += result[element_var.name]

        return [
            [s, None, None]
        ]


    # ('avg', E1, E2, [body-atoms])
    # returns the average of results of the values of E2 in body-atoms in E1
    def avg(self, values: list, context: ExecutionContext) -> list[list]:

        sum_var, element_var, body = values

        results = context.solver.solve(body, context.binding)

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
    def percentage(self, values: list, context: ExecutionContext) -> list[list]:

        pecentage_var, nominator, denominator = values

        nominator_results = context.solver.solve(nominator, context.binding)
        denominator_results = context.solver.solve(denominator, context.binding)

        if len(denominator_results) == 0:
            return []

        percentage = (len(nominator_results) / len(denominator_results)) * 100.0

        return [
            [percentage, None, None]
        ]


    # ('not', [body-atoms])
    # if body-atoms returns values, not returns an empty list
    # otherwise, it returns a list with a single value: True
    def not_function(self, values: list, context: ExecutionContext) -> list[list]:

        body = values[0]

        results = context.solver.solve(body, context.binding)
        count = len(results)

        if count > 0:
            return []
        else:
            return [
                [True]
            ]


    # ('=', E1, 5)
    def assign(self, values: list, context: ExecutionContext) -> list[list]:

        return [[
            values[1], values[1]
        ]]


    # ('det_equals', [body-atoms], E2)
    def determiner_equals(self, values: list, context: ExecutionContext) -> list[list]:

        body, number = values

        results = context.solver.solve(body, context.binding)
        count = len(results)

        if count == number:
            return results
        else:
            return []


    # ('det_greater_than', [body-atoms], E2)
    def determiner_greater_than(self, values: list, context: ExecutionContext) -> list[list]:

        body, number = values

        results = context.solver.solve(body, context.binding)
        count = len(results)

        if count > number:
            return results
        else:
            return []


    # ('all', E1, [range-atoms], [body-atoms])
    def determiner_all(self, values: list, context: ExecutionContext) -> list[list]:

        # find_var, quant, body = values
        # predicate1, quant_var, det, nbar = quant

        quant_var, range, body = values

        entities = OrderedSet([binding[quant_var.name] for binding in context.solver.solve(range, context.binding)])

        # print(entities)

        range_count = len(entities)
        results = OrderedSet()
        for entity in entities:
            b = context.binding | {
                quant_var.name: entity
            }
            bindings = context.solver.solve(body, b)
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
    def determiner_none(self, values: list, context: ExecutionContext) -> list[list]:

        body = values[0]

        results = context.solver.solve(body, context.binding)
        count = len(results)

        if count == 0:
            return [
                [True, None, None]
            ]
        else:
            return []        
        