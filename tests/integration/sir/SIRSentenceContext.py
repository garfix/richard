from richard.entity.Relation import Relation
from richard.module.SimpleMemoryModule import SimpleMemoryModule


class SIRSentenceContext(SimpleMemoryModule):

    def __init__(self) -> None:
        super().__init__()
        self.add_relation(Relation("format", arguments=["type"]))
        self.add_relation(Relation("format_canned", arguments=["response"]))
        self.add_relation(Relation("format_number", arguments=["variable", "unit"]))
