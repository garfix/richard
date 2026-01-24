from richard.entity.Relation import Relation
from richard.module.BasicOutputBuffer import BasicOutputBuffer


class SIROutputBuffer(BasicOutputBuffer):

    def __init__(self) -> None:
        super().__init__()

        self.add_relation(Relation("output_count", formal_parameters=["number"]))
        self.add_relation(Relation("output_how_many", formal_parameters=["type1", "type2"]))
        self.add_relation(Relation("output_dont_know_part_of", formal_parameters=["type1", "type2"]))
        self.add_relation(Relation("output_location", formal_parameters=["object"]))

        # helper to use `left of` in the "broader sense" using transitivity
        self.add_relation(Relation("context", formal_parameters=["type"]))
