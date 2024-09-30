

from richard.entity.Relation import Relation
from richard.entity.Variable import Variable
from richard.interface.SomeModule import SomeModule
from richard.type.ExecutionContext import ExecutionContext
from richard.type.OrderedSet import OrderedSet


class CoreModule(SomeModule):

    isolated_queries_cache: dict

    def __init__(self) -> None:
        self.relations = {
            "==": Relation(query_function=self.equals),
            ">": Relation(query_function=self.greater_than),
            "<": Relation(query_function=self.less_than),
            "arg_min": Relation(query_function=self.arg_min),
            "arg_max": Relation(query_function=self.arg_max),
            "sum": Relation(query_function=self.sum),
            "avg": Relation(query_function=self.avg),
            "percentage": Relation(query_function=self.percentage),
            "count": Relation(query_function=self.count),
            "not": Relation(query_function=self.not_function),
            "=": Relation(query_function=self.assign),
            "det_equals": Relation(query_function=self.determiner_equals),
            "det_greater_than": Relation(query_function=self.determiner_greater_than),
            "det_less_than": Relation(query_function=self.determiner_less_than),
            "all": Relation(query_function=self.determiner_all),
            "none": Relation(query_function=self.determiner_none),
            "isolated": Relation(query_function=self.isolated),
            "store": Relation(query_function=self.store),
        }

        self.isolated_queries_cache = {}


    # ('==', E1, E2)
    def equals(self, values: list, context: ExecutionContext) -> list[list]:

        e1 = values[0]
        e2 = values[1]

        if e1 is None:
            if e2 is None:
                raise Exception("== is called with two variables")
            else:
                return [[e2, e2]]
        else:
            if e2 is None:
                return [[e1, e1]]

        if e1 == e2:
            return [[e1, e2]]
        return []


    # ('>', E1, E2)
    # E1 and E2 must be bound
    def greater_than(self, values: list, context: ExecutionContext) -> list[list]:

        e1 = values[0]
        e2 = values[1]

        if e1 is None:
            raise Exception("> first argument is unbound")
        if e2 is None:
            raise Exception("> second argument is unbound")

        if e1 > e2:
            return [values]
        return []


    # ('<', E1, E2)
    # E1 and E2 must be bound
    def less_than(self, values: list, context: ExecutionContext) -> list[list]:

        e1 = values[0]
        e2 = values[1]

        if e1 is None:
            raise Exception("< first argument is unbound")
        if e2 is None:
            raise Exception("< second argument is unbound")

        if e1 < e2:
            return [values]
        return []


    # ('count', E1, [body-atoms])
    # returns the number of results of body-atoms in E1
    def count(self, values: list, context: ExecutionContext) -> list[list]:

        body = values[1]

        results = context.solver.solve(body, context.binding)
        count = len(results)

        return [
            [count, None]
        ]


    # ('sum', E1, E2, [body-atoms])
    # returns the sum of results of the values of E2 in body-atoms in E1
    def sum(self, values: list, context: ExecutionContext) -> list[list]:

        element_var = context.arguments[1]
        body = values[2]

        results = context.solver.solve(body, context.binding)
        s = 0
        for result in results:
            s += result[element_var.name]

        return [
            [s, None, None]
        ]


    # ('arg_min', E1, E2, [body-atoms])
    # returns the minimum value of results of the values of E2 in body-atoms in E1
    def arg_min(self, values: list, context: ExecutionContext) -> list[list]:

        min_var = context.arguments[0]
        element_var = context.arguments[1]
        body = values[2]

        results = context.solver.solve(body, context.binding)

        if len(results) == 0:
            return []

        min = None
        entity = None
        for result in results:
            if min is None or result[element_var.name] < min:
                min = result[element_var.name]
                entity = result[min_var.name]

        return [
            [entity, min, None]
        ]


    # ('arg_max', E1, E2, [body-atoms])
    # returns the maximum value of results of the values of E2 in body-atoms in E1
    def arg_max(self, values: list, context: ExecutionContext) -> list[list]:

        max_var = context.arguments[0]
        element_var = context.arguments[1]
        body = values[2]

        results = context.solver.solve(body, context.binding)

        if len(results) == 0:
            return []

        max = None
        entity = None
        for result in results:
            if max is None or result[element_var.name] > max:
                max = result[element_var.name]
                entity = result[max_var.name]

        return [
            [entity, max, None]
        ]


    # ('avg', E1, E2, [body-atoms])
    # returns the average of results of the values of E2 in body-atoms in E1
    def avg(self, values: list, context: ExecutionContext) -> list[list]:

        element_var = context.arguments[1]
        body = values[2]

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

        nominator = values[1]
        denominator = values[2]

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
                [None]
            ]


    # ('=', E1, 5)
    def assign(self, values: list, context: ExecutionContext) -> list[list]:

        return [
            [values[1], values[1]]
        ]


    # ('det_equals', [body-atoms], E2)
    def determiner_equals(self, values: list, context: ExecutionContext) -> list[list]:

        body, number = values

        results = context.solver.solve(body, context.binding)
        count = len(results)

        if count == number:
            return [
                [None, None]
            ]
        else:
            return []


    # ('det_greater_than', [body-atoms], E2)
    def determiner_greater_than(self, values: list, context: ExecutionContext) -> list[list]:

        body, number = values

        results = context.solver.solve(body, context.binding)
        count = len(results)

        if count > number:
            return [
                [None, None]
            ]
        else:
            return []


    # ('det_less_than', [body-atoms], E2)
    def determiner_less_than(self, values: list, context: ExecutionContext) -> list[list]:

        body, number = values

        results = context.solver.solve(body, context.binding)
        count = len(results)

        if count < number:
            return [
                [None, None]
            ]
        else:
            return []


    # ('all', E1, [range-atoms], [body-atoms])
    def determiner_all(self, values: list, context: ExecutionContext) -> list[list]:

        quant_var = context.arguments[0]
        range = values[1]
        body = values[2]

        entities = OrderedSet([binding[quant_var.name] for binding in context.solver.solve(range, context.binding)])

        range_count = len(entities)
        results = OrderedSet()
        for entity in entities:
            b = context.binding | {
                quant_var.name: entity
            }
            bindings = context.solver.solve(body, b)
            if len(bindings) > 0:
                results.add(entity)

        result_count = len(results)

        success = result_count == range_count

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
                [None]
            ]
        else:
            return []


    # ('isolated', [body-atoms])
    def isolated(self, values: list, context: ExecutionContext) -> list[list]:
        body = values[0]

        key = str(body) + str(context.binding)
        if key in self.isolated_queries_cache:
            return self.isolated_queries_cache[key]
        else:
            results = context.solver.solve(body, context.binding)
            count = len(results)

        if count == 0:
            result = []
        else:
            result = [
                [None]
            ]

        self.isolated_queries_cache[key] = result

        return result


    # ('store', atom)
    def store(self, values: list, context: ExecutionContext) -> list[list]:
        atom = values[0]

        context.solver.write_atom(atom)

        return [
            [None]
        ]

