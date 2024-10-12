from richard.entity.Relation import Relation
from richard.interface.SomeDataSource import SomeDataSource
from richard.interface.SomeModule import SomeModule
from richard.type.ExecutionContext import ExecutionContext


class CooperModule(SomeModule):

    ds: SomeDataSource


    def __init__(self, data_source: SomeDataSource) -> None:

        self.ds = data_source
        self.relations = {
            "resolve_name": Relation(query_function=self.resolve_name),
            "not_3v": Relation(query_function=self.not_3v),
            "and_3v": Relation(query_function=self.and_3v),
            "metal": Relation(query_function=self.common_query, write_function=self.common_write, attributes=['entity', 'truth']),
            "element": Relation(query_function=self.common_query, write_function=self.common_write, attributes=['entity', 'truth']),
            "nonmetal": Relation(query_function=self.common_query, write_function=self.common_write, attributes=['entity', 'truth']),
            "white": Relation(query_function=self.common_query, write_function=self.common_write, attributes=['entity', 'truth']),
            "oxide": Relation(query_function=self.common_query, write_function=self.common_write, attributes=['entity', 'truth']),
            "burns_rapidly": Relation(query_function=self.common_query, write_function=self.common_write,  attributes=['entity', 'truth']),
        }


    def resolve_name(self, values: list, context: ExecutionContext) -> list[list]:
        name = values[0].lower()

        out_values = self.ds.select("name", ["name", "id"], [name, None])
        if len(out_values) > 0:
            return out_values
        else:
            id = context.arguments[1].name
            self.ds.insert("name", ["name", "id", ], [name, id])
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
        results = self.ds.select(context.predicate, context.relation.attributes, values)
        if len(results) > 0:
            return results
        else:
            return [
                values[:-1] + ["unknown"]
            ]


    def common_write(self, values: list, context: ExecutionContext) -> list[list]:
        # print(context.predicate, values)
        self.ds.insert(context.predicate, context.relation.attributes, values)

