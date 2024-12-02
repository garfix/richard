from richard.entity.Relation import Relation
from richard.module.SimpleMemoryModule import SimpleMemoryModule


class SIRDialogContext(SimpleMemoryModule):

    def __init__(self) -> None:
        super().__init__()
        self.add_relation(Relation("isa", arguments=["entity", "type"]))

