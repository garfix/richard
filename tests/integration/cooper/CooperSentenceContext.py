from richard.entity.Relation import Relation
from richard.module.SimpleMemoryModule import SimpleMemoryModule


class CooperSentenceContext(SimpleMemoryModule):

    def __init__(self) -> None:
        super().__init__({
            "format": Relation(attributes=["type"]),
            "format_ynu": Relation(attributes=["answer"]),
            "format_canned": Relation(attributes=["response"]),
        })
