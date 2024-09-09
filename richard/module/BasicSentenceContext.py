from richard.entity.Relation import Relation
from richard.module.SimpleMemoryModule import SimpleMemoryModule


class BasicSentenceContext(SimpleMemoryModule):

    def __init__(self) -> None:
            super().__init__({
                "format": Relation(attributes=["type"]),
                "format_list": Relation(attributes=["variable"]),
                "format_table": Relation(attributes=["variables", "units"]),
                "format_number": Relation(attributes=["variable", "unit"]),
            })

