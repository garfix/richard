from richard.entity.Relation import Relation
from richard.module.SimpleMemoryModule import SimpleMemoryModule


class WikidataSentenceContext(SimpleMemoryModule):

    def __init__(self) -> None:
        super().__init__()

        self.clear()

        self.add_relation(Relation("output_type", arguments=["type"]))
        self.add_relation(Relation("output_report", arguments=["report"]))


    def clear(self):
        super().clear()

        cursor = self.data_source.connection.cursor()

        cursor.execute("CREATE TABLE output_type (type TEXT)")
        cursor.execute("CREATE TABLE output_report (report TEXT)")

