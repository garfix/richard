from richard.entity.Relation import Relation
from richard.module.SimpleMemoryModule import SimpleMemoryModule


class BasicSentenceContext(SimpleMemoryModule):

    def __init__(self) -> None:
        super().__init__()
        self.add_relation(Relation("format", attributes=["type"]))
        self.add_relation(Relation("format_list", attributes=["variable"]))
        self.add_relation(Relation("format_table", attributes=["variables", "units"]))
        self.add_relation(Relation("format_number", attributes=["variable", "unit"]))
        self.add_relation(Relation("format_canned", attributes=["response"]))

