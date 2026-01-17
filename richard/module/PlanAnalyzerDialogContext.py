from richard.entity.Relation import Relation
from richard.module.SimpleMemoryModule import SimpleMemoryModule


class PlanAnalyzerDialogContext(SimpleMemoryModule):
    def __init__(self) -> None:
        super().__init__()

        self.clear()

        self.add_relation(Relation("goal", arguments=["event_id"]))


    def clear(self):
        super().clear()

        cursor = self.data_source.connection.cursor()

        cursor.execute("CREATE TABLE goal (event_id TEXT)")
