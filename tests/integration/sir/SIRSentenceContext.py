from richard.entity.Relation import Relation
from richard.module.SimpleMemoryModule import SimpleMemoryModule


class SIRSentenceContext(SimpleMemoryModule):

    def __init__(self) -> None:
        super().__init__()

        self.clear()

        self.add_relation(Relation("output_type", arguments=["type"]))
        self.add_relation(Relation("output_count", arguments=["number"]))


    def clear(self):
        super().clear()

        cursor = self.data_source.connection.cursor()

        cursor.execute("CREATE TABLE output_type (type TEXT)")
        cursor.execute("CREATE TABLE output_count (number INT)")

