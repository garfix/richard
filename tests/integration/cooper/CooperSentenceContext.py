from richard.entity.Relation import Relation
from richard.module.SimpleMemoryModule import SimpleMemoryModule


class CooperSentenceContext(SimpleMemoryModule):

    def __init__(self) -> None:
        super().__init__()
        self.add_relation(Relation("format", attributes=["type"]))
        self.add_relation(Relation("format_ynu", attributes=["answer"]))
        self.add_relation(Relation("format_canned", attributes=["response"]))

