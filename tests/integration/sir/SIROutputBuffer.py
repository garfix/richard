from richard.entity.Relation import Relation
from richard.module.BasicOutputBuffer import BasicOutputBuffer


class SIROutputBuffer(BasicOutputBuffer):

    def __init__(self) -> None:
        super().__init__()

        self.add_relation(Relation("output_count", arguments=["number"]))
        self.add_relation(Relation("output_how_many", arguments=["type1", "type2"]))
        self.add_relation(Relation("output_dont_know_part_of", arguments=["type1", "type2"]))
        self.add_relation(Relation("output_location", arguments=["object"]))

        # helper to use `left of` in the "broader sense" using transitivity
        self.add_relation(Relation("context", arguments=["type"]))
