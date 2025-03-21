from richard.entity.Relation import Relation
from richard.interface.SomeDataSource import SomeDataSource
from richard.interface.SomeModule import SomeModule
from richard.type.ExecutionContext import ExecutionContext


class CooperModule(SomeModule):

    ds: SomeDataSource


    def __init__(self, data_source: SomeDataSource) -> None:
        super().__init__()
        self.ds = data_source
        self.add_relation(Relation("resolve_name", query_function=self.resolve_name))
        self.add_relation(Relation("not_3v", query_function=self.not_3v))
        self.add_relation(Relation("and_3v", query_function=self.and_3v))
        self.add_relation(Relation("metal", query_function=self.common_query, write_function=self.common_write, arguments=['entity', 'truth']))
        self.add_relation(Relation("element", query_function=self.common_query, write_function=self.common_write, arguments=['entity', 'truth']))
        self.add_relation(Relation("compound", query_function=self.common_query, write_function=self.common_write, arguments=['entity', 'truth']))
        self.add_relation(Relation("nonmetal", query_function=self.common_query, write_function=self.common_write, arguments=['entity', 'truth']))
        self.add_relation(Relation("white", query_function=self.common_query, write_function=self.common_write, arguments=['entity', 'truth']))
        self.add_relation(Relation("dark_gray", query_function=self.common_query, write_function=self.common_write, arguments=['entity', 'truth']))
        self.add_relation(Relation("brittle", query_function=self.common_query, write_function=self.common_write, arguments=['entity', 'truth']))
        self.add_relation(Relation("oxide", query_function=self.common_query, write_function=self.common_write, arguments=['entity', 'truth']))
        self.add_relation(Relation("sulfide", query_function=self.common_query, write_function=self.common_write, arguments=['entity', 'truth']))
        self.add_relation(Relation("chloride", query_function=self.common_query, write_function=self.common_write, arguments=['entity', 'truth']))
        self.add_relation(Relation("fuel", query_function=self.common_query, write_function=self.common_write,  arguments=['entity', 'truth']))
        self.add_relation(Relation("burns", query_function=self.common_query, write_function=self.common_write,  arguments=['entity', 'truth']))
        self.add_relation(Relation("burns_rapidly", query_function=self.common_query, write_function=self.common_write,  arguments=['entity', 'truth']))
        self.add_relation(Relation("combustable", query_function=self.common_query, write_function=self.common_write,  arguments=['entity', 'truth']))
        self.add_relation(Relation("gasoline", query_function=self.common_query, write_function=self.common_write,  arguments=['entity', 'truth']))


    def resolve_name(self, values: list, context: ExecutionContext) -> list[list]:
        name = values[0].lower()
        id = values[1]

        out_values = self.ds.select("entity", ["name", "id"], [name, None])
        if len(out_values) > 0:
            return out_values
        else:
            # if id is given, a new name is linked to that id
            if id is None:
                # otherwise a new id is created for the name
                id = context.arguments[1].name
            self.ds.insert("entity", ["name", "id", ], [name, id])
            return [
                [name, id]
            ]


    # ('not_3v', in, out)
    def not_3v(self, values: list, context: ExecutionContext) -> list[list]:

        value = values[0]

        if value == 'true':
            return [
                [None, 'false']
            ]
        elif value == 'false':
            return [
                [None, 'true']
            ]
        else:
            return [
                [None, 'unknown']
            ]


    # ('and_3v', in1, in2, out)
    def and_3v(self, values: list, context: ExecutionContext) -> list[list]:

        in1, in2, _ = values

        if in1 == 'true' and in2 == 'false':
            return [[None, None, 'false']]
        elif in1 == 'true' and in2 == 'unknown':
            return [[None, None, 'unknown']]
        elif in1 == 'true' and in2 == 'true':
            return [[None, None, 'true']]

        elif in1 == 'false' and in2 == 'false':
            return [[None, None, 'false']]
        elif in1 == 'false' and in2 == 'unknown':
            return [[None, None, 'unknown']]
        elif in1 == 'false' and in2 == 'true':
            return [[None, None, 'false']]

        elif in1 == 'unknown' and in2 == 'false':
            return [[None, None, 'unknown']]
        elif in1 == 'unknown' and in2 == 'unknown':
            return [[None, None, 'unknown']]
        elif in1 == 'unknown' and in2 == 'true':
            return [[None, None, 'unknown']]


    def common_query(self, values: list, context: ExecutionContext) -> list[list]:
        results = self.ds.select(context.relation.predicate, context.relation.arguments, values)
        if len(results) > 0:
            return results
        else:
            return [
                values[:-1] + ["unknown"]
            ]


    def common_write(self, values: list, context: ExecutionContext) -> list[list]:
        self.ds.insert(context.relation.predicate, context.relation.arguments, values)

