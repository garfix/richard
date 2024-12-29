from richard.entity.ProcessingException import ProcessingException
from richard.entity.Relation import Relation
from richard.entity.ResultIterator import ResultIterator
from richard.entity.Variable import Variable
from richard.interface.SomeDataSource import SomeDataSource
from richard.interface.SomeModule import SomeModule
from richard.type.ExecutionContext import ExecutionContext


class SIRModule(SomeModule):

    ds: SomeDataSource


    def __init__(self, data_source: SomeDataSource) -> None:
        super().__init__()
        self.ds = data_source
        self.add_relation(Relation("resolve_name", query_function=self.resolve_name))
        self.add_relation(Relation("finger", query_function=self.finger))
        self.add_relation(Relation("have", query_function=self.have))
        self.add_relation(Relation("part_of", query_function=self.common_query, write_function=self.common_write, arguments=['part', 'whole'])),
        self.add_relation(Relation("part_of_n", query_function=self.part_of_n, write_function=self.common_write, arguments=['part', 'whole', 'number'])),
        self.add_relation(Relation("isa", query_function=self.common_query, write_function=self.common_write, arguments=['entity', 'type'])),
        self.add_relation(Relation("equals", query_function=self.common_query, write_function=self.common_write, arguments=['entity1', 'entity2'])),
        self.add_relation(Relation("own", query_function=self.common_query, write_function=self.common_write, arguments=['person', 'thing'])),


    def common_query(self, values: list, context: ExecutionContext) -> list[list]:
        results = self.ds.select(context.relation.predicate, context.relation.arguments, values)
        return results


    def common_write(self, values: list, context: ExecutionContext) -> list[list]:
        self.ds.insert(context.relation.predicate, context.relation.arguments, values)


    def part_of_n(self, values: list, context: ExecutionContext) -> list[list]:
        part_variable = context.arguments[0]
        whole_variable = context.arguments[1]

        results = self.ds.select(context.relation.predicate, context.relation.arguments, values)

        if len(results) == 0:
            whole_type = None
            if isinstance(whole_variable, Variable):
                whole_type = self.get_name(context, whole_variable.name, values[1])

            part_type = None
            if isinstance(part_variable, Variable):
                part_type = self.get_name(context, part_variable.name, values[0])

            raise ProcessingException(f"How many {part_type} per {whole_type}?")

        return results


    # ('create_relation', predicate, arguments)
    def create_relation(self, values: list, context: ExecutionContext) -> list[list]:

        predicate, arguments = values

        self.add_relation(Relation(predicate, arguments=arguments, query_function=self.common_query, write_function=self.common_write))

        return [
            [None, None]
        ]


    # resolve(name, id)
    def resolve_name(self, values: list, context: ExecutionContext) -> list[list]:
        name = values[0]

        return [
            [None, name]
        ]


    # finger(id)
    def finger(self, values: list, context: ExecutionContext) -> list[list]:

        # no individual fingers are available, but we must return at least one
        return [
            ['a-finger']
        ]


    # have(whole, part)
    # the verb have is always very abstract, but in this case it also handles with information on the class-level
    def have(self, values: list, context: ExecutionContext) -> list[list]:

        # solving based on class information

        whole_variable = context.arguments[0]
        part_variable = context.arguments[1]

        whole_type = None
        if isinstance(whole_variable, Variable):
            whole_type = self.get_name(context, whole_variable.name, values[0])

        part_type = None
        if isinstance(part_variable, Variable):
            part_type = self.get_name(context, part_variable.name, values[1])

        results = context.solver.solve([('part_of_number', part_type, whole_type, Variable('N'))])

        if len(results) == 0:
            raise ProcessingException(f"Don't know whether {part_type} is part of {whole_type}")

        number = results[0]['N']
        response = ResultIterator([None, None], number)

        return response


    def get_name(self, context: ExecutionContext, id: str, value):
        # try to find the class
        isa = context.solver.solve1([('isa', id, Variable('Type'))])
        if isa:
            type = isa["Type"]
            if type == 'person':
                return value
            else:
                return type

        return value

