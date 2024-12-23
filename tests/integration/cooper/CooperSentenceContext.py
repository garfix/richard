from richard.entity.Relation import Relation
from richard.module.SimpleMemoryModule import SimpleMemoryModule


class CooperSentenceContext(SimpleMemoryModule):

    def __init__(self) -> None:
        super().__init__()

        self.clear()

        self.add_relation(Relation("format", arguments=["type"]))
        self.add_relation(Relation("format_ynu", arguments=["answer"]))
        self.add_relation(Relation("format_canned", arguments=["response"]))


    def clear(self):
        super().clear()

        cursor = self.data_source.connection.cursor()

        cursor.execute("CREATE TABLE format (type TEXT)")
        cursor.execute("CREATE TABLE format_ynu (answer TEXT)")
        cursor.execute("CREATE TABLE format_canned (response TEXT)")
