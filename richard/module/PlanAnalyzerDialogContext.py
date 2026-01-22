from richard.data_source.SimpleFrameDataSource import SimpleFrameDataSource
from richard.entity.Relation import Relation
from richard.interface.SomeModule import SomeModule
from richard.module.SqliteMemoryModule import SqliteMemoryModule


class PlanAnalyzerDialogContext(SomeModule):

    data_source: SimpleFrameDataSource

    def __init__(self) -> None:
        super().__init__()
        self.data_source = SimpleFrameDataSource()

        self.add_relation(Relation("goal", arguments=["event_id"]))


    def clear(self):
        self.data_source.clear()

