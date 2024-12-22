from richard.entity.Relation import Relation
from richard.module.SimpleMemoryModule import SimpleMemoryModule


class BasicDialogContext(SimpleMemoryModule):

    def __init__(self) -> None:
        super().__init__()
        self.add_relation(Relation("dialog_isa", arguments=["entity", "type"]))

