from richard.entity.Relation import Relation
from richard.interface.SomeDataSource import SomeDataSource
from richard.interface.SomeModule import SomeModule
from richard.entity.ExecutionContext import ExecutionContext


class HelloWorldModule(SomeModule):

    ds: SomeDataSource


    def __init__(self, data_source: SomeDataSource) -> None:
        super().__init__()
        self.ds = data_source
        self.add_relation(Relation("river", query_function=self.simple_entity))


    def simple_entity(self, arguments: list, context: ExecutionContext) -> list[list]:
        return self.ds.select(context.relation.predicate, ["id"], arguments)
