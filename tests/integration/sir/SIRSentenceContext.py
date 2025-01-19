from richard.entity.Relation import Relation
from richard.module.BasicSentenceContext import BasicSentenceContext


class SIRSentenceContext(BasicSentenceContext):

    def __init__(self) -> None:
        super().__init__()

        self.add_relation(Relation("output_count", arguments=["number"]))
        self.add_relation(Relation("output_how_many", arguments=["type1", "type2"]))
        self.add_relation(Relation("output_dont_know_part_of", arguments=["type1", "type2"]))
