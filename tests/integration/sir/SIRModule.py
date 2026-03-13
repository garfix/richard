from richard.entity.BindingResult import BindingResult
from richard.entity.Relation import Relation
from richard.entity.Variable import Variable
from richard.interface.SomeDataSource import SomeDataSource
from richard.interface.SomeModule import SomeModule
from richard.entity.ExecutionContext import ExecutionContext


class SIRModule(SomeModule):

    ds: SomeDataSource


    def __init__(self, data_source: SomeDataSource) -> None:
        super().__init__()
        self.ds = data_source
        self.add_relation(Relation("resolve_name", query_function=self.resolve_name))
        self.add_relation(Relation("finger", query_function=self.finger))
        self.add_relation(Relation("have", query_function=self.have))
        self.add_relation(Relation("part_of", query_function=self.common_query, write_function=self.common_write, formal_parameters=['part', 'whole'])),
        self.add_relation(Relation("part_of_n", query_function=self.part_of_n, write_function=self.common_write, formal_parameters=['part', 'whole', 'number'])),
        self.add_relation(Relation("isa", query_function=self.common_query, write_function=self.common_write, formal_parameters=['entity', 'type'])),
        self.add_relation(Relation("identical", query_function=self.common_query, write_function=self.common_write, formal_parameters=['entity1', 'entity2'])),
        self.add_relation(Relation("own", query_function=self.common_query, write_function=self.common_write, formal_parameters=['person', 'thing'])),
        self.add_relation(Relation("just_left_of", query_function=self.common_query, write_function=self.common_write, formal_parameters=['thing1', 'thing2'])),
        self.add_relation(Relation("left_of", query_function=self.common_query, write_function=self.common_write, formal_parameters=['thing1', 'thing2'])),

        # used in write_grammar.py
        self.add_relation(Relation("position_description", query_function=self.position_description, formal_parameters=['description'])),


    def common_query(self, arguments: list, context: ExecutionContext) -> list[list]:
        results = self.ds.select(context.relation.predicate, context.relation.formal_parameters, arguments)
        return results


    def common_write(self, arguments: list, context: ExecutionContext) -> list[list]:
        self.ds.insert(context.relation.predicate, context.relation.formal_parameters, arguments)


    def part_of_n(self, arguments: list, context: ExecutionContext) -> list[list]:
        part_variable = arguments[0]
        whole_variable = arguments[1]

        whole_type = whole_variable
        part_type = self.get_type(context, part_variable, part_variable)


        results = self.ds.select(context.relation.predicate, context.relation.formal_parameters, arguments)

        if len(results) == 0:
            if part_type is not None and whole_type is not None:

                # produce output
                context.solver.solve([('store', [('output_type', 'how_many'), ('output_how_many', part_type, whole_type)])])

        return results


    # ('create_relation', predicate, arguments)
    def create_relation(self, arguments: list, context: ExecutionContext) -> list[list]:

        predicate, arguments = arguments

        self.add_relation(Relation(predicate, formal_parameters=arguments, query_function=self.common_query, write_function=self.common_write))

        return [
            [None, None]
        ]


    # resolve(name, id)
    def resolve_name(self, arguments: list, context: ExecutionContext) -> list[list]:
        name = arguments[0]

        return [
            [None, name]
        ]


    # finger(id)
    def finger(self, arguments: list, context: ExecutionContext) -> list[list]:

        # no individual fingers are available, but we must return at least one
        return [
            ['a-finger']
        ]


    # have(whole, part)
    # the verb have is always very abstract, but in this case it also handles with information on the class-level
    def have(self, arguments: list, context: ExecutionContext) -> list[list]:

        # solving based on class information

        whole_variable = arguments[0]
        part_variable = arguments[1]

        whole_type = whole_variable
        part_type = self.get_type(context, part_variable, part_variable)
        results = context.solver.solve([('part_of_number', part_type, whole_type, Variable('N'))])

        if len(results) == 0:
            # produce output
            context.solver.solve([('store', [('output_type', 'dont_know_part_of'), ('output_dont_know_part_of', part_type, whole_type)])])
            return []

        number = results[0]['N']

        return BindingResult([{'A': n} for n in range(number)])


    def get_type(self, context: ExecutionContext, id: str, value):
        if id == 'a-finger':
            return 'finger'

        return value


    # used in write_grammar.py to create complex output
    def position_description(self, arguments: list, context: ExecutionContext) -> list[list]:
        # working out the algorithm described in the article is left to the interested reader
        return [
            ['<the ordered list>']
        ]

