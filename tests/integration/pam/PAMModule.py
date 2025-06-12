from richard.entity.Relation import Relation
from richard.interface.SomeDataSource import SomeDataSource
from richard.interface.SomeModule import SomeModule
from richard.type.ExecutionContext import ExecutionContext


class PAMModule(SomeModule):

    ds: SomeDataSource


    def __init__(self, data_source: SomeDataSource) -> None:
        super().__init__()
        self.ds = data_source
        self.add_relation(Relation("river", query_function=self.simple_entity))
        self.add_relation(Relation("resolve_name", query_function=self.resolve_name))


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
                [None, id]
            ]


    def simple_entity(self, values: list, context: ExecutionContext) -> list[list]:
        return self.ds.select(context.relation.predicate, ["id"], values)
