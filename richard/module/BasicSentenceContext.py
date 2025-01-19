from richard.entity.Relation import Relation
from richard.module.SimpleMemoryModule import SimpleMemoryModule


class BasicSentenceContext(SimpleMemoryModule):

    def __init__(self) -> None:
        super().__init__()

        self.clear()

        self.add_relation(Relation("output_type", arguments=["type"]))
        self.add_relation(Relation("output_number", arguments=["number"]))
        self.add_relation(Relation("output_name_not_found", arguments=["name"]))


    def clear(self):
        super().clear()

        cursor = self.data_source.connection.cursor()

        cursor.execute("CREATE TABLE output_type (type TEXT)")
        cursor.execute("CREATE TABLE output_number (number FLOAT)")
        cursor.execute("CREATE TABLE output_name_not_found (name TEXT)")
