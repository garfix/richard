from richard.entity.Relation import Relation
from richard.module.SimpleMemoryModule import SimpleMemoryModule


class CooperSentenceContext(SimpleMemoryModule):

    def __init__(self) -> None:
        super().__init__()
        self.add_relation(Relation("format", arguments=["type"]))
        self.add_relation(Relation("format_ynu", arguments=["answer"]))
        self.add_relation(Relation("format_canned", arguments=["response"]))

