from richard.entity.Relation import Relation
from richard.module.SimpleMemoryModule import SimpleMemoryModule


class Chat80DialogContext(SimpleMemoryModule):

    def __init__(self) -> None:
        super().__init__({
            "isa": Relation(attributes=["entity", "type"]),
        })
