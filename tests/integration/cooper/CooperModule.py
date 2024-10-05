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
            "isa": Relation(query_function=self.isa_query, write_function=self.isa_write),
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


    def isa_query(self, values: list, context: ExecutionContext) -> list[list]:
        entity, type, truth = values

        results = self.ds.select("isa", ["entity", "type", "truth"], [entity, type, truth])
        if len(results) > 0:
            return results
        else:
            return [
                [None, None, "unknown"]
            ]


    def isa_write(self, values: list, context: ExecutionContext) -> list[list]:
        entity, type, truth = values

        self.ds.insert("isa", ["entity", "type", "truth"], [entity, type, truth])
