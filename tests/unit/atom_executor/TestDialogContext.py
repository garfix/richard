from richard.entity.Relation import Relation
from richard.module.SimpleMemoryModule import SimpleMemoryModule


class TestDialogContext(SimpleMemoryModule):

    def __init__(self) -> None:
        super().__init__()
        cursor = self.data_source.connection.cursor()

        cursor.execute("CREATE TABLE isa (entity TEXT, type TEXT)")
        cursor.execute("CREATE TABLE continent (entity TEXT)")
        cursor.execute("CREATE TABLE concept (type TEXT)")

        self.add_relation(Relation("isa", arguments=["entity", "type"]))
        self.add_relation(Relation("continent", arguments=["entity"]))
        self.add_relation(Relation("concept", arguments=["type"]))

