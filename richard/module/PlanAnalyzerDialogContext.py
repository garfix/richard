from richard.data_source.SimpleFrameDataSource import SimpleFrameDataSource
from richard.entity.ExecutionContext import ExecutionContext
from richard.entity.Relation import Relation
from richard.interface.SomeModule import SomeModule


class PlanAnalyzerDialogContext(SomeModule):

    data_source: SimpleFrameDataSource

    def __init__(self) -> None:
        super().__init__()
        self.data_source = SimpleFrameDataSource()

        self.add_relation(Relation("goal_episode", formal_parameters=["event_id"], query_function=self.query, write_function=self.write))


    def query(self, arguments: list, context: ExecutionContext) -> list[list]:
        return self.data_source.select(context.relation.predicate, context.relation.formal_parameters, arguments)


    def write(self, arguments: list, context: ExecutionContext):
        self.data_source.insert(context.relation.predicate, context.relation.formal_parameters, arguments)


    def clear(self):
        self.data_source.clear()

