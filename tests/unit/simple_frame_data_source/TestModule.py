from richard.data_source.SimpleFrameDataSource import SimpleFrameDataSource
from richard.entity.Relation import Relation
from richard.interface.SomeModule import SomeModule
from richard.entity.ExecutionContext import ExecutionContext


class TestModule(SomeModule):

    data_source: SimpleFrameDataSource

    def __init__(self, data_source: SimpleFrameDataSource) -> None:
        super().__init__()
        self.data_source = data_source

        self.add_relation(Relation("goal", query_function=self.query, write_function=self.write))


    def query(self, values: list, context: ExecutionContext) -> list[list]:
        return self.data_source.select(context.relation.predicate, context.relation.arguments, values)


    def write(self, values: list, context: ExecutionContext):
        self.data_source.insert(context.relation.predicate, context.relation.arguments, values)
