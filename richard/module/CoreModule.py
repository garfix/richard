

from richard.core.atoms import bind_variables
from richard.entity.Relation import Relation
from richard.entity.Variable import Variable
from richard.interface.SomeModule import SomeModule
from richard.type.ExecutionContext import ExecutionContext
from richard.type.OrderedSet import OrderedSet


class CoreModule(SomeModule):

    def __init__(self) -> None:
        super().__init__()
        self.add_relation(Relation("equals", query_function=self.equals)),
        self.add_relation(Relation("greater_than", query_function=self.greater_than)),
        self.add_relation(Relation("less_than", query_function=self.less_than)),
        self.add_relation(Relation("multiply", query_function=self.multiply)),
        self.add_relation(Relation("arg_min", query_function=self.arg_min)),
        self.add_relation(Relation("arg_max", query_function=self.arg_max)),
        self.add_relation(Relation("sum", query_function=self.sum)),
        self.add_relation(Relation("avg", query_function=self.avg)),
        self.add_relation(Relation("percentage", query_function=self.percentage)),
        self.add_relation(Relation("count", query_function=self.count)),
        self.add_relation(Relation("not", query_function=self.not_function)),
        self.add_relation(Relation("let", query_function=self.let)),
        self.add_relation(Relation("det_equals", query_function=self.determiner_equals)),
        self.add_relation(Relation("det_greater_than", query_function=self.determiner_greater_than)),
        self.add_relation(Relation("det_less_than", query_function=self.determiner_less_than)),
        self.add_relation(Relation("all", query_function=self.determiner_all)),
        self.add_relation(Relation("none", query_function=self.determiner_none)),
        self.add_relation(Relation("scoped", query_function=self.scoped)),
        self.add_relation(Relation("store", query_function=self.store)),
        self.add_relation(Relation("destructure", query_function=self.destructure)),
        self.add_relation(Relation("find_all", query_function=self.find_all)),
        self.add_relation(Relation("find_one", query_function=self.find_one)),


    # ('equals', E1, E2)
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


    # ('greater_than', E1, E2)
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


    # ('less_than', E1, E2)
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


    # ('multiply', E1, E2, E3)
    # E3 is set to E1 * E2
    def multiply(self, values: list, context: ExecutionContext) -> list[list]:

        e1 = values[0]
        e2 = values[1]
        e3 = e1 * e2

        if e1 is None:
            raise Exception("* first argument is unbound")
        if e2 is None:
            raise Exception("* second argument is unbound")

        return [
            [None, None, e3]
        ]


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
        # print(values, context.binding, results)
        count = len(results)

        if count > 0:
            return []
        else:
            return [
                [None]
            ]


    # ('let', E1, 5)
    def let(self, values: list, context: ExecutionContext) -> list[list]:

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


    # ('scoped', [body-atoms])
    # a wrapper around a possibly variable list of atoms
    def scoped(self, values: list, context: ExecutionContext) -> list[list]:
        body = values[0]

        results = context.solver.solve(body, context.binding)
        count = len(results)

        if count == 0:
            result = []
        else:
            result = [
                [None]
            ]

        return result


    # ('store', [body-atoms])
    def store(self, values: list, context: ExecutionContext) -> list[list]:

        unbound_atoms = values[0]

        if not isinstance(unbound_atoms, list):
            raise Exception(f"'store' expects a list of atoms; given: {unbound_atoms}")

        atoms = bind_variables(unbound_atoms, context.binding)

        for atom in atoms:
            context.solver.write_atom(atom)

        return [
            [None]
        ]


    # ('destructure', body-atoms, term, term, term...)
    # for example: ('destructure', Atom, 'just_left_of', A, B)
    def destructure(self, values: list, context: ExecutionContext) -> list[list]:

        unbound_atoms = values[0]
        atoms = bind_variables(unbound_atoms, context.binding)
        atom = atoms[0]
        structure = context.arguments[1:]
        fail_structure = [None] + [None] * len(structure)

        if len(atom) != len(structure):
            return [ fail_structure ]

        result = [None]
        for atom_term, structure_term in zip(atom, structure):
            if atom_term == structure_term:
                new_term = structure_term
            else:
                if isinstance(structure_term, Variable):
                    new_term = atom_term
                else:
                    return [ fail_structure ]

            result.append(new_term)

        return [
            result
        ]


    # ('findall', variable-name, body-atoms, result-variable)
    # ('findall', [variable-name, variable-name...], body-atoms, result-variable)
    # Creates a list of all values of variable found by running body-atoms
    # There can be a list of variables, in which case a list of combinations is returned
    # Returned value is placed in result-variable
    def find_all(self, values: list, context: ExecutionContext) -> list[list]:

        variable = values[0]
        body = values[1]
        is_list = isinstance(variable, list)

        result = []

        for binding in context.solver.solve(body, context.binding):
            if is_list:
                item = []
                for v in variable:
                    if v in binding:
                        item.append(binding[v])
                    else:
                        item.append(None)
                # skip duplicates
                if not item in result:
                    result.append(item)
            else:
                # skip duplicates
                if variable in binding:
                    item = binding[variable]
                    if not item in result:
                        result.append(item)

        return [
            [None, None, result]
        ]


    # ('find_one', variable-name, body-atoms, result-variable)
    # ('fine_one', [variable-name, variable-name...], body-atoms, result-variable)
    # Returns only the first value (values) of the results.
    # Useful if you know there's only one result and you're don't want a list
    # There can be a list of variables, in which case a list of combinations is returned
    # Returned value is placed in result-variable
    def find_one(self, values: list, context: ExecutionContext) -> list[list]:

        results = self.find_all(values, context)
        if len(results[0][2]) == 0:
            return []
        else:
            return [
                [None, None, results[0][2][0]]
            ]
