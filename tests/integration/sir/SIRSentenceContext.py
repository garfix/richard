from richard.entity.Relation import Relation
from richard.module.BasicSentenceContext import BasicSentenceContext


class SIRSentenceContext(BasicSentenceContext):

    def __init__(self) -> None:
        super().__init__()

        self.clear()

        self.add_relation(Relation("output_count", arguments=["number"]))
        self.add_relation(Relation("output_how_many", arguments=["type1", "type2"]))
        self.add_relation(Relation("output_dont_know_part_of", arguments=["type1", "type2"]))


    def clear(self):
        super().clear()

        cursor = self.data_source.connection.cursor()

        cursor.execute("CREATE TABLE output_count (number INT)")
        cursor.execute("CREATE TABLE output_how_many (type1 TEXT, type2 TEXT)")
        cursor.execute("CREATE TABLE output_dont_know_part_of (type1 TEXT, type2 TEXT)")

